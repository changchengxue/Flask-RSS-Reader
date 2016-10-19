from flaskmarks import db, config
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import desc


class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.Unicode(255), nullable=False)
    title = db.Column(db.Unicode(255), nullable=False)
    url = db.Column(db.Unicode(512), nullable=False)
    tags = db.Column(db.Unicode(512))
    clicks = db.Column(db.Integer, default=0)
    last_clicked = db.Column(db.DateTime)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    @classmethod
    def by_tag(cls, page, oID, per_page, tag):
        tag = "%"+tag+"%"
        return cls.query.filter(and_(
                                 cls.tags.like(tag),
            cls.owner_id == oID))\
                         .order_by(desc(cls.clicks))\
                         .paginate(page, per_page, False)

    @classmethod
    def by_string(cls, page, oID, per_page, string, marktype=False):
        string = "%"+string+"%"
        base = cls.query.filter(cls.owner_id == oID)\
                         .filter(or_(cls.title.like(string),
                                     cls.tags.like(string),
                                     cls.url.like(string)))
        if marktype:
            base = base.filter(cls.type == marktype)
        base = base.order_by(desc(cls.clicks))\
                   .paginate(page, per_page, False)
        return base

    def __repr__(self):
        return '<Mark {}>'.format(self.title)
