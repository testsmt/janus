(assert (forall ((x Bool)) (let ((y x)) (or y (not y)))))
(check-sat)
