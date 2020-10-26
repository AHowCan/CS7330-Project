# Set to True to use local settings, will overwrite any setting in config with same name
USE_LOCAL_CONFIG = True

# replace user:password with your user and password
# note that this is not the user/password to login to cloud.mongodb.com
# but rather the user/password defined in cloud.mongodb.com - Database Access
CLOUD_URI = 'mongodb+srv://user:password@cluster0.0qxsh.mongodb.net/bus_network?retryWrites=true&w=majority'

LOCAL_URI = 'mongodb://localhost:27017/'

DB_URI = CLOUD_URI
# for a local db uncomment the next line
#DB_URI = LOCAL_URI
