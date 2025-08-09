# Assumptions

- Two rigid humanoids, inflexible links, limited joint ranges from URDF
- Initial friction small but non-zero to approximate no-gi mats; configurable and can be annealed
- Hierarchical reward priorities: top > control > joint hyperextension > choke
- Self-play both agents train concurrently
- GUI available for debugging; headless for training
- Python 3.12 environment; developer uses Windows PowerShell

<!-- EOF -->
