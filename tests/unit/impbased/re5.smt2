(assert (str.in_re "abc" (re.++ (str.to_re "a") (str.to_re "b") (str.to_re "c"))))
(check-sat)
