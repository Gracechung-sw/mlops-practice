pip install locust==1.4.1
pip install pandas==0.23.3
docker pull origin master
locust -f locust/locustfile.py --host http://127.0.0.1:5050