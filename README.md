
## Require

- luckmake > 0.0.6 
```bash
TAG=0.0.6
# TAG=master  # for development branch
curl -sL https://github.com/shouldsee/luck/archive/${TAG}.tar.gz -o luck-${TAG}.tar.gz
tar -xvzf luck-${TAG}.tar.gz
cd luck-${TAG}/
install -m 755 bin/luck* $HOME/.local/bin

luckmake -V ## to test accessibility
```

## Available Commands:

```bash
luckmake clean
luckmake build
```