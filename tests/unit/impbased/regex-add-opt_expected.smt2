(assert (str.in_re "a" (re.opt (str.to_re "a"))))
(check-sat)
