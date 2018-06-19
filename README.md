My personal blog.

Pelican conf files, plugins, theme, and pipfiles are in `pelican/`. Source markdown posts are in `pelican/posts/`. Run `pelican` in the `pelican/` directory (after `pipenv shell`ing) to generate test files into `pelican/tmp`. Run the `publish.sh` script to generate the files into the root directory, commit, and push.

The `pelican/pelican-plugins` directory is a git submodule, so you will either need to do `git clone --recursive` (optionally with the --shallow-submodules option) or `git submodule update --init` if the repo is already cloned.
