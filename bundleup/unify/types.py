"""
Typed shapes for Unify API responses.

These TypedDicts mirror the response schemas defined in the BundleUp API
(workers/unify/src/routes/*.ts). They exist purely for static analysis
(mypy) - the SDK still returns plain dicts at runtime via response.json(),
so adding these costs nothing and changes no behavior.

If the API response shape changes, update the matching TypedDict here.
"""

from typing import Any, Dict, List, Optional, TypedDict


class Metadata(TypedDict):
    next: Optional[str]


# Identity

class Account(TypedDict):
    id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    avatar_url: Optional[str]


class MeResponse(TypedDict):
    data: Account


# Chat

class ChatUser(TypedDict):
    id: str
    name: str


class ChatChannel(TypedDict):
    id: str
    name: str


class UsersResponse(TypedDict):
    data: List[ChatUser]
    metadata: Metadata


class ChannelsResponse(TypedDict):
    data: List[ChatChannel]
    metadata: Metadata


class MessageResponse(TypedDict):
    data: Dict[str, Any]


# CRM

class CrmCompany(TypedDict):
    id: str
    name: str
    website: Optional[str]


class CrmContact(TypedDict):
    id: str
    name: str
    email: Optional[str]


class CompaniesResponse(TypedDict):
    data: List[CrmCompany]
    metadata: Metadata


class ContactsResponse(TypedDict):
    data: List[CrmContact]
    metadata: Metadata


# Drive

class DriveFile(TypedDict):
    id: str
    name: str
    mime_type: Optional[str]
    size: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    url: Optional[str]
    is_folder: bool


class FilesResponse(TypedDict):
    data: List[DriveFile]
    metadata: Metadata


# Git

class GitRepo(TypedDict):
    id: Any  # numeric for GitHub/GitLab, string UUID for Bitbucket
    name: str
    full_name: str
    description: Optional[str]
    url: str
    created_at: str
    updated_at: str
    pushed_at: str


class GitPull(TypedDict):
    id: int
    number: int
    title: str
    description: Optional[str]
    draft: bool
    state: str
    url: str
    user: str
    created_at: str
    updated_at: str
    merged_at: Optional[str]


class GitTag(TypedDict):
    name: str
    commit_sha: str


class GitRelease(TypedDict):
    id: int
    name: str
    tag_name: str
    description: str
    prerelease: bool
    url: str
    created_at: str
    released_at: str


class GitBranch(TypedDict):
    name: str
    commit_sha: str
    protected: bool


class GitCommit(TypedDict):
    sha: str
    message: Optional[str]
    url: str
    author: Optional[str]
    author_email: Optional[str]
    committed_at: Optional[str]


class ReposResponse(TypedDict):
    data: List[GitRepo]
    metadata: Metadata


class PullsResponse(TypedDict):
    data: List[GitPull]
    metadata: Metadata


class TagsResponse(TypedDict):
    data: List[GitTag]
    metadata: Metadata


class ReleasesResponse(TypedDict):
    data: List[GitRelease]
    metadata: Metadata


class BranchesResponse(TypedDict):
    data: List[GitBranch]
    metadata: Metadata


class CommitsResponse(TypedDict):
    data: List[GitCommit]
    metadata: Metadata


# Project Management

class TicketingTicket(TypedDict):
    id: str
    title: str
    status: str
    url: str
    description: Optional[str]
    created_at: str
    updated_at: str


class TicketsResponse(TypedDict):
    data: List[TicketingTicket]
    metadata: Metadata
