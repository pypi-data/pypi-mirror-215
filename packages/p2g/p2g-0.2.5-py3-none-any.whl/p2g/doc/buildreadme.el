(progn
  (add-to-list 'load-path "/home/sac/.emacs.d/straight/build/ox-gfm") 
  (require 'ox-gfm)
  (setq org-confirm-babel-evaluate nil)  
  (find-file "p2g/doc/readme.org")
  (org-gfm-export-to-markdown))

  
