---
title: Better Remote Access
type: docs
sidebar:
  open: true
---

The BioHPC has some quality-of-life things that makes remoting into the servers a lot easier. This outlines
some of the things that reduce the friction of remote access.

1. You can set up an SSH key on your local machine and save it with BioHPC for password-free login
- https://biohpc.cornell.edu/lab/ssh_keys.aspx <- full instructions, pretty simple
- Select "Terminal (ssh command via Mac...)" from the dropdown
2. You can use your laptop/computer's hardware encryption instead of the 2-factor Duo authentication (Win/Mac)
- Select "Hardware-backed secure keys (2FA Alternative)" from the drop down
3. You can SSH into BioHPC off campus without VPN by logging into the login node (cbsulogin.biohpc.cornell.edu) and ssh-ing into whatever specific server you want
4. You can shortcut ssh-ing altogether by setting up `~/.ssh/config` with all your SSH targets and specific configurations for them.
- This can automate bullets 1 and 3, plus additional perks like logging into a specific shell (e.g. ZSH)
- e.g. You can rename `cbsugenomics2.biohpc.cornell.edu`  "Genomics2", so that it can be accessed
more simply by calling
```bash
ssh Genomics2
```

### An actual config:
This are the contents of file `~/.ssh/config`:
```
Host Nina
    HostName cbsunt246.tc.cornell.edu
    User pd348
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    RequestTTY force
    RemoteCommand zsh -l
    ProxyJump Cornell

Host Cornell
    Hostname cbsulogin.biohpc.cornell.edu
    User pd348
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    RequestTTY force
```

The ssh-tunneling described above is achieved by the `ProxyJump` line provided under `Nina`, where it first connects to `Cornell`, and from there jumps into `Nina`. So, a very real world case is simply:
```bash
ssh Nina
```
That's it. It seems to work for VScode and Zed editors as well.