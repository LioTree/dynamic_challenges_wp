from CTFd.models import db,Challenges

class WriteupDynamicChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "wp_dynamic"}
    id = db.Column(db.Integer, db.ForeignKey("challenges.id",ondelete="CASCADE"), primary_key=True)
    initial = db.Column(db.Integer, default=0)
    minimum = db.Column(db.Integer, default=0)
    decay = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(WriteupDynamicChallenge, self).__init__(**kwargs)
        self.value = kwargs["initial"]

def query_challenge(cid):
    challenge = db.session.query(Challenges).filter_by(id=cid).first()
    return challenge

class Writeup(db.Model):
    # __mapper_args__ = {"polymorphic_identity": "writeups"}
    wid = db.Column(db.Integer,primary_key=True)
    cid = db.Column(db.Integer,db.ForeignKey("challenges.id",ondelete="CASCADE"),nullable=False)
    uid = db.Column(db.Integer,nullable=False)
    tid = db.Column(db.Integer,nullable=True)
    path = db.Column(db.String(200),nullable=False)

    def __init__(self,cid,uid,tid,path):
        self.cid = int(cid)
        self.uid = int(uid)
        self.tid = int(tid) if tid else None
        self.path = path

def insert_writeup(cid,uid,tid,path):
    wp = Writeup(cid,uid,tid,path)
    db.session.add(wp)
    db.session.commit()

def query_writeup(cid,uid,tid):
    if tid == None:
        wp = db.session.query(Writeup).filter_by(cid=cid,uid=uid).first()
    else:
        wp = db.session.query(Writeup).filter_by(cid=cid,tid=tid).first()
    return wp