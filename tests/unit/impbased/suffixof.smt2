(declare-fun a () String)
(declare-fun b () String)
(assert (str.suffixof a b))
(check-sat)
