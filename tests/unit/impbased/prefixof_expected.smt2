(declare-fun a () String)
(declare-fun b () String)
(assert (<= (str.len a) (str.len b)))
(check-sat)
