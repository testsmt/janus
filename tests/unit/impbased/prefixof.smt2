(declare-fun a () String)
(declare-fun b () String)
(assert (str.prefixof a b))
(check-sat)
