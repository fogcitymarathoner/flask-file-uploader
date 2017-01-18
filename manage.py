from flask_script import Manager

from app import app
from lib.cors import PolicySigner

manager = Manager(app)


@manager.command
def policy_signature(expire_seconds):
    """
    prints policy and signature for expire_seconds into future
    """
    print('Servicing S3 Bucket %s Branch %s' % (app.config['AWS_BUCKET'], app.config['BRANCH']))
    signer = PolicySigner(
        int(expire_seconds), app.config['AWS_BUCKET'], app.config['BRANCH'], app.config['AWS_ACCESS_KEY_ID'],
        app.config['AWS_SECRET_ACCESS_KEY'])
    print(signer.to_table())


if __name__ == "__main__":
    manager.run()
