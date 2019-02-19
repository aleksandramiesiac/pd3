# Jeśli lista nie jest pusta, to tylko te fora zostaną przerobione
co_przerobic = []

# Jeśli powyższa lista jest pusta, to zostaną przerobione wszystkie fora poza tymi wypisanymi w poniższej liście
co_wykluczyc = ["stackoverflow", "stackoverflow.meta", "stackoverflowES", "stackoverflowES.meta", "stackoverflowJA", "stackoverflowJA.meta", "stackoverflowPT", "stackoverflowPT.meta", "stackoverflowRU", "stackoverflowRU.meta"]

# Które kolumny wydobyć z danego pliku
Badges_all = ['Id', 'UserId', 'Name', 'Date', 'Class', 'TagBased']
Comments_all = ['Id', 'PostId', 'Score', 'Text', 'CreationDate', 'UserId']
PostHistory_all = ['Id', 'PostHistoryTypeId', 'PostId', 'RevisionGUID', 'CreationDate', 'UserId', 'Comment', 'Text']
PostLinks_all = ['Id', 'CreationDate', 'PostId', 'RelatedPostId', 'LinkTypeId']
Posts_all = ['Id', 'PostTypeId', 'AcceptedAnswerId', 'ParentId', 'CreationDate', 'Score', 'ViewCount', 'Body', 'OwnerUserId', 'LastEditorUserId', 'LastEditDate', 'LastActivityDate', 'Title', 'Tags', 'AnswerCount', 'CommentCount', 'FavoriteCount', 'ClosedDate', 'CommunityOwnedDate']
Tags_all = ['Id', 'TagName', 'Count', 'ExcerptPostId', 'WikiPostId']
Users_all = ['Id', 'Reputation', 'CreationDate', 'DisplayName', 'LastAccessDate', 'WebsiteUrl', 'Location', 'AboutMe', 'Views', 'UpVotes', 'DownVotes', 'ProfileImageUrl', 'AccountId']
Votes_all = ['Id', 'PostId', 'VoteTypeId', 'UserId', 'CreationDate', 'BountyAmount']

co_wydobyc = {
    "Badges": Badges_all,
    "Comments": Comments_all,
    "PostHistory": [], #PostHistory_all
    "PostLinks": [], #PostLinks_all,
    "Posts": Posts_all,
    "Tags": Tags_all,
    "Users": Users_all, #["AccountId", "Id", "DisplayName"],
    "Votes": Votes_all
}
