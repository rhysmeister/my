##############################################################
# Configuration for the cluster. auth_details must be shared #
# across the cluster.                                        #
# MariaDB user created as                                    #
# CREATE USER pycluster@'%' IDENTIFIED BY 'secret';          #
# GRANT PROCESS, REPLICATION CLIENT,                         #
# REPLICATION SLAVE ON *.* TO pycluster@'%';                 #
##############################################################
cluster = [
                { "hostname": "master", "port": 3306 },
                { "hostname": "master2", "port": 3306 },
                { "hostname": "slave1", "port": 3306 },
                { "hostname": "slave2", "port": 3306 } ]
auth_details = {
                "username": "pycluster",
                "password": "secret"
        }
##############################################################

