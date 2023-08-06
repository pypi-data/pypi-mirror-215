This module is designed to work with .vcfg configs.

# All commands:
Create a new promotion: new(<name>, <text>)
Get information: get(<name>)
Change action: set(<name>, <text>)

# Example:
```
# Import the library and create a variable for convenience
import vconfig_by_mrwoon as config
cfg = config.Configs("config.vcfg")

# Create a new group
cfg.new("name", "Vasya")

# Display concentration on the screen
print(cfg.get("name"))```