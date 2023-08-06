import json
import tornado
import shlex
import sqlalchemy
import subprocess

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join

from .db_handler import DBHandler, Runs

class RouteHandler(APIHandler):
    db = DBHandler()


    def getRuns(self):
        runs_list = []
        with self.db.get_session() as session:
            for run in session.query(Runs).all():
                runs_list.append(run.serialize())
        return runs_list
        

    @tornado.web.authenticated  # type: ignore
    def get(self):
        try:
            runs = self.getRuns()
            self.finish(json.dumps(runs))
        except Exception as e:
            self.log.info(f"There has been an exception reading the jupyterlab-nbqueue db => {e}")


    @tornado.web.authenticated
    def post(self):
        try:
            request_data = self.get_json_body()
            notebook = request_data.get('notebook', None)                
            if notebook:
                cmd_split = shlex.split(f'jupyter nbconvert --to notebook --execute ./{notebook}')
                process = subprocess.Popen(cmd_split, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                success = True
        except subprocess.CalledProcessError as exc:
            self.log.error(f"Program failed {exc.returncode} - {exc}")
            message = f"Program failed {exc.returncode} - {exc}"
        except subprocess.TimeoutExpired as exc:
            self.log.error(f"Program timed out {exc}")
            message = f"Program timed out {exc}"
        except Exception as exc:
            self.log.error(f"Exception {exc}")
            message = f"Exception {exc}"
        else:
            success = True
        finally:
            with self.db.get_session() as session:
                if process:
                    new_process = Runs(pid=process.pid, name=notebook, status='', message='')
                    new_process.status = 'Running' if success else 'Error'
                    new_process.message = '' if success else message
                    session.add(new_process)
                    session.commit()
                                
                    out, error = process.communicate()

                    if error.strip() != '':
                        session.query(Runs).filter_by(pid=process.pid).update({'status': 'Error', 'message': error.strip().decode('utf-8')})

                    if out.strip() != '':
                        session.query(Runs).filter_by(pid=process.pid).update({'status': 'Finished'})

                    session.commit()
                else:
                    self.log.error('It has not been possible to execute the command. It must be related to the OS')


        self.finish(json.dumps({
            "data": "This is /jupyterlab-nbqueue/run endpoint!"
        }))

    @tornado.web.authenticated  # type: ignore
    def delete(self):
        try:
            request_data = self.get_json_body()
            if request_data:
                delete_all = request_data['deleteAll']
                if delete_all:
                    with self.db.get_session() as session:
                        session.query(Runs).delete()
                        session.commit()
                        message = "All Deleted."
                else:
                    id_to_del = request_data['id']
                    pid_to_del = request_data['pid']
                    with self.db.get_session() as session:
                        download_to_delete = session.query(Runs).filter(Runs.id == id_to_del, Runs.pid == pid_to_del).first()
                        if download_to_delete:
                            session.delete(download_to_delete)
                            session.commit()
                            message = "Delete."
                        else:
                            message = "Not Deleted"
            else:
                message = "There has been an error with the data sent to the backend. Please check with your administrator"
        except sqlalchemy.exc.IntegrityError as e:   # type: ignore
            self.log.error(f'Integrity Check failed => {e}')
            self.finish(json.dumps([]))  
        except Exception as e:
            self.log.error(f"There has been an error deleting downloaded => {e}")
        else:
            self.finish(json.dumps(message))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    handlers = [
        (url_path_join(base_url, "jupyterlab-nbqueue", "run"), RouteHandler)
    ]
    web_app.add_handlers(host_pattern, handlers)