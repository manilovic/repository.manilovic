#!/bin/bash



git config --global user.email "juanma_fr@hotmail.com"
git config --global user.name "manilovic"


git add .
git commit -m "Commit $(date)"



GIT_SSH_COMMAND="ssh -i /home/juan.gonzalez/.ssh/git -o StrictHostKeyChecking=no" git push origin master
