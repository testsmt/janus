(declare-fun a () String)
(declare-fun b () String)
(assert (str.contains a b))
(check-sat)
