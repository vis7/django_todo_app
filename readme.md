# ToDo
Basic ToDo Application

# functionality
1)Login/register with email verification

2)Todo add/update/delete, category, due date and status wise

3) Todo sharing
- Any user can share his/her todo with other system user
- User can give various access like read only, read/write and need approval after updating any todo
- For approval, if any user changes the shared todo, the owner needs to approve the changes. Owner can approve or reject the changes

4) Access log
- Here, user will see various activities regarding his/her shared todo
- Like, when the todo was updated etc

# Superuser
username - admin
password - admin

# test scenario
## Scenario1
- user1 create and share todo1 with user2
- user2 make changes in todo1 
- user1 approve changes of user2

## Scenario2
- user2 create and share todo2 with user1
- user1 make changes in todo2
- user2 reject changes of user1

# Extenstions
- for sorting imports
```
isort .
```

# Upgrades
- add linter
