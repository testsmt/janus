(assert (not (str.in_re "a" (re.range "t" "z"))))
(assert (not (str.in_re "4" (re.range "0" "3"))))
(check-sat)
