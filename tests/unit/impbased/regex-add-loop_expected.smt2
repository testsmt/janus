(assert (str.in_re "a" ((_ re.loop 1 39) (str.to_re "a"))))
(check-sat)
