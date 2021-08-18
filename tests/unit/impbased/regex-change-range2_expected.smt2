(assert (not (str.in_re "a" (re.range (ite (and (= (str.len "z") 1) (str.<= "t" "z")) "z" "t") "z"))))
(assert (not (str.in_re "4" (re.range (ite (and (= (str.len "t") 1) (str.<= "0" "t")) "t" "0") "3"))))
(check-sat)
