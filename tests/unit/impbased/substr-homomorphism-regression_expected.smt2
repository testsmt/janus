(declare-const s String)
(assert (= s "abc"))
(assert (=> (and (>= 2 0) (>= 1 0)) (str.suffixof (str.substr s 2 (str.len s)) (str.substr s 1 (str.len s)))))
(check-sat)
