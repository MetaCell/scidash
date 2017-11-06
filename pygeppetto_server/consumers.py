import json


def ws_connect(message):
    print('Socket opened')
    # Accept the connection request
    message.reply_channel.send({'accept': True})

    # 1 -> Send the connection
    message.reply_channel.send({
            'text': json.dumps({
                'type': 'client_id',
                'data': json.dumps({
                    'clientID': 'Connection1'
                    })
                })
            })
    # 2 -> Check user privileges
    message.reply_channel.send({
            'text': json.dumps({
                'type': 'user_privileges',
                'data': json.dumps({
                    "user_privileges": json.dumps({
                        "userName": "Python User",
                        "loggedIn": True,
                        "hasPersistence": False,
                        "privileges": [
                            "READ_PROJECT",
                            "DOWNLOAD",
                            "DROPBOX_INTEGRATION",
                            "RUN_EXPERIMENT",
                            "WRITE_PROJECT"
                            ]
                        })
                    })
                })
            })


def ws_receive(message):
    payload = json.loads(message['text'])
    if (payload['type'] == 'geppetto_version'):
        print("Geppetto Version 0.3.7")
        # Where do we get the geppetto version from?
        message.reply_channel.send({
            "text": json.dumps({
                "requestID": payload['requestID'],
                "type": "geppetto_version",
                "data": json.dumps({
                    "geppetto_version": "0.3.7"
                    })
                })
            })


def ws_disconnect(message):
    print("Socket closed")
