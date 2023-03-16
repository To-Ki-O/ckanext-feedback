from datetime import datetime

from ckan.model.package import Package
from ckan.model.resource import Resource

from ckanext.feedback.models.session import session
from ckanext.feedback.models.utilization import (
    Utilization,
    UtilizationComment,
    UtilizationCommentCategory,
)


# Get details from the Utilization record
def get_utilization(utilization_id):
    return (
        session.query(
            Utilization.title,
            Utilization.description,
            Utilization.approval,
            Resource.name.label('resource_name'),
            Resource.id.label('resource_id'),
            Package.name.label('package_name'),
        )
        .join(Resource, Resource.id == Utilization.resource_id)
        .join(Package, Package.id == Resource.package_id)
        .filter(Utilization.id == utilization_id)
        .first()
    )


# Approve currently displayed utilization
def approve_utilization(utilization_id, approval_user_id):
    utilization = session.query(Utilization).get(utilization_id)
    utilization.approval = True
    utilization.approved = datetime.now()
    utilization.approval_user_id = approval_user_id


# Get comments related to the Utilization record
def get_utilization_comments(utilization_id, approval=None):
    query = (
        session.query(UtilizationComment)
        .filter(UtilizationComment.utilization_id == utilization_id)
        .order_by(UtilizationComment.created.desc())
    )
    if approval is not None:
        query = query.filter(UtilizationComment.approval == approval)

    return query.all()


# Create comment for currently displayed utilization
def create_utilization_comment(utilization_id, category, content):
    comment = UtilizationComment(
        utilization_id=utilization_id,
        category=category,
        content=content,
    )
    session.add(comment)


# Approve selected utilization comment
def approve_utilization_comment(comment_id, approval_user_id):
    comment = session.query(UtilizationComment).get(comment_id)
    comment.approval = True
    comment.approved = datetime.now()
    comment.approval_user_id = approval_user_id


# Get comment category enum names and values
def get_utilization_comment_categories():
    return UtilizationCommentCategory
