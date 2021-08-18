(assert (str.in_re "x" (re.inter (str.to_re "x") (str.to_re "x"))))
(check-sat)
