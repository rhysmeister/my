##############################################################
# Configuration for the cluster. auth_details must be shared #
# across the cluster.                                        #
# MariaDB user created as                                    #
# CREATE USER pycluster@'%' IDENTIFIED BY 'secret';          #
# GRANT PROCESS, REPLICATION CLIENT,                         #
# REPLICATION SLAVE ON *.* TO pycluster@'%';                 #
##############################################################
cluster = [
                { "hostname": "srucidmdbmb1", "port": 3306 },
                { "hostname": "srucidmdbmb2", "port": 3306 },
                { "hostname": "srucidmdbsb1", "port": 3306 },
                { "hostname": "srucidmdbsb2", "port": 3306 },
		{ "hostname": "srucidmdbbckb1", "port": 3306 },
		{ "hostname": "hostdoesnotexist", "port": 3306 },
		{ "hostname": "srucidmdbbckb1", "port": 12345 }
        ]

auth_details = {
                "username": "pycluster",
                "password": "1BlVwSzrrcO7Yc864nvv"
        }
##############################################################

