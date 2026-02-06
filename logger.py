# =============================================
# Module to implement idiomatic Python logging
# =============================================

import sys

# Test commit
# Another commit here...
import logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    handlers = [logging.StreamHandler(sys.stdout)],
    force = True 
)

logger = logging.getLogger(__name__)
