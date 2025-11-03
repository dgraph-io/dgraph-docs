# Dgraph Documentation

## Contribution guidelines

As a contributor to Dgraph documentation, we ask that you do the following:

- **Develop in the `main` branch **

Refer to the README from main branch.

The master branch is used by the CI to build the documentation from the branches `releases/vX.Y`.
The script build.sh is doing the work.

To test the build locally from the master branch:
```bash
 ./scripts/build.sh http://localhost:3000
 ```

 To build the doc using local baseURL.

 Then
 ```
 cd public
 python3 -m http.server 3000
 ```
 to serve the static pages locally.

 Note: from main branch you can directly use `hugo serve` to build and serve.


