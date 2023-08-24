# Testing 

## Testing within container 

Since we use containers to wrap the project, you can run tests in the `fce-bot` container using: 

```commandline
docker exec -it fce-bot python -m pytest 
```