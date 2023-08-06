import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ...models import GitHubOrg as GitHubOrgModel
from ...models import GitHubOrgMembership as GitHubOrgMembershipModel
from ...models import GitHubToken as GitHubTokenModel
from ...models import GitHubUser as GitHubUserModel
from ..connection import CountedConnection
from ..filter_ import PFilterableConnectionField


class GitHubOAuthAppInfo(graphene.ObjectType):
    client_id = graphene.String()
    authorize_url = graphene.String()
    redirect_uri = graphene.String()


class AuthPayload(graphene.ObjectType):
    token = graphene.String()


class GitHubToken(SQLAlchemyObjectType):
    class Meta:
        model = GitHubTokenModel
        interfaces = (relay.Node,)
        exclude_fields = [
            "token",
        ]
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory

    token_masked = graphene.String()

    def resolve_token_masked(parent, info):
        return "X" * 15


class GitHubUser(SQLAlchemyObjectType):
    class Meta:
        model = GitHubUserModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class GitHubOrg(SQLAlchemyObjectType):
    class Meta:
        model = GitHubOrgModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory


class GitHubOrgMembership(SQLAlchemyObjectType):
    class Meta:
        model = GitHubOrgMembershipModel
        interfaces = (relay.Node,)
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory
