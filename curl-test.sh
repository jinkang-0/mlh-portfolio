#!/bin/bash

echo "Assessing initial state..."
INIT_LEN=$(curl http://localhost:5000/api/timeline_post | jq '.timeline_posts | length')

echo "Creating test data..."
POST_REQ=$(curl -X POST http://localhost:5000/api/timeline_post -d "name=Test&email=test@example.com&content=This is a test post")
POST_REQ_ID=$(jq '.id' <<< "$POST_REQ")

echo "Checking if post was created..."
CURR_DATA=$(curl http://localhost:5000/api/timeline_post)
CURR_LEN=$(jq '.timeline_posts | length' <<< "$CURR_DATA")
if ! [[ $CURR_LEN == $((INIT_LEN + 1)) ]]; then
  echo "Expected length to be $((INIT_LEN + 1)), but got $CURR_LEN"
  exit 1
fi

# check if the post was created
POST_CONTENT=$(jq ".timeline_posts | map(select(.id = $POST_REQ_ID))" <<< "$CURR_DATA")
if [[ -z $POST_CONTENT ]]; then
  echo "Post with ID $POST_REQ_ID was not created"
  exit 1
fi

echo "Deleting test data..."
DELETE_REQ=$(curl -X DELETE http://localhost:5000/api/timeline_post -d "id=$POST_REQ_ID")

echo "Checking if post was deleted..."
CURR_DATA=$(curl http://localhost:5000/api/timeline_post)
CURR_LEN=$(jq '.timeline_posts | length' <<< "$CURR_DATA")
if ! [[ $CURR_LEN == $INIT_LEN ]]; then
  echo "Expected length to be $INIT_LEN, but got $CURR_LEN"
  exit 1
fi

echo "Test passed"
