from pymongo import MongoClient
import sys
import datetime


class database(object):
	def __init__(self, args):
		self._client = MongoClient() 
		self.args = args
		self.Connect_db()

	def __del__(self):
		self.Close_conn()

	def Close_conn(self):
		self._client.close()
		print('Connection closed')

	def Connect_db(self):
		if self.args.get('name') is None:
			name = datetime.datetime.now()
			self.args.update({'name':'database'+name.isoformat()[:10]})
		self.db = self._client[self.args['name']]
		print('Database connected: ', self.args['name'])
		
def main():
	if len(sys.argv) == 1:
	    print("Usage: mongo.py [argument1=value argument2=value ...]\narguments:\naddress=host:port  default localhost:27017\ndb=db_name  default random_name\n")
	else: 
		argumets = {}
		for a in range(1,len(sys.argv)):
			a1, a2 = sys.argv[a].split("=")
			argumets.update({a1:a2})	
		print(argumets)

if __name__ == '__main__':
	main()