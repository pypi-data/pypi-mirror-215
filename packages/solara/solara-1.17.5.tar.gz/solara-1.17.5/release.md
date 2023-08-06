
# Fully automated

    $ ./release.sh patch


## Making an alpha release


    $ ./release.sh patch --new-version 1.17.5a1


# semi automated
To make a new release
```
# update solara/__init__.py
$ git add -u && git commit -m 'Release v1.17.5' && git tag v1.17.5 && git push upstream master v1.17.5
```


If a problem happens, and you want to keep the history clean
```
# do fix
$ git rebase -i HEAD~3
$ git tag v1.17.5 -f &&  git push upstream master v1.17.5 -f
```
