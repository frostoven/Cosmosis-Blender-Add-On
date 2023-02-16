## Format

Blender does not support text in versioning, but Cosmosis already uses text in
versions. To work around this, replace the following words with the following
numbers:
```
alpha | versions 1-10: 1-10
beta  | versions 1-10: 100-110
rc    | versions 1-10: 1000-1010
```

That should hopefully allow us enough leeway to not run into numbering
problems.

The plugin's own version is place behind the version of Cosmosis it targets.

## Example

Suppose our plugin is version `1.0.0` and target Cosmosis `0.74.0-beta.1`. The
Blender version should look like this:
```
bl_info.version: (0, 74, 0, 100, 1, 0, 0)
Blender add-ons screen: 
File name: CosmosisDev_0.74.0-beta.1__1.0.0
```
