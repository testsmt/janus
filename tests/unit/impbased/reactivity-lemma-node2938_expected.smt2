(set-info :smt-lib-version 2.6)
(set-logic NRA)
(set-info :source |
These benchmarks used in the paper:

  Dejan Jovanovic and Leonardo de Moura.  Solving Non-Linear Arithmetic.
  In IJCAR 2012, published as LNCS volume 7364, pp. 339--354.

The keymaera family contains VCs from Keymaera verification, see:

  A. Platzer, J.-D. Quesel, and P. Rummer.  Real world verification.
  In CADE 2009, pages 485-501. Springer, 2009.

Submitted by Dejan Jovanovic for SMT-LIB.

 KeYmaera example: reactivity-lemma, node 2938 For more info see: @see "Andre Platzer and Jan-David Quesel. European Train Control System: A case study in formal verification. In Karin Breitman and Ana Cavalcanti, editors, 11th International Conference on Formal Engineering Methods, ICFEM, Rio de Janeiro, Brasil, Proceedings, volume 5885 of LNCS, pages 246-265. Springer, 2009."
|)
(set-info :category "industrial")
(set-info :status sat)
(declare-fun v () Real)
(declare-fun d () Real)
(declare-fun b () Real)
(declare-fun Z1uscore0 () Real)
(declare-fun t1uscore0 () Real)
(declare-fun ep () Real)
(declare-fun ts1uscore0 () Real)
(declare-fun M1uscore0 () Real)
(declare-fun amax () Real)
(declare-fun SB () Real)
(assert (not (exists ((t1uscore0 Real)) (forall ((ts1uscore0 Real)) (let ((?v_2 (* 2.0 b)) (?v_1 (* d d)) (?v_0 (+ (* amax t1uscore0) v))) (=> (and (and (and (and (and (=> (>= t1uscore0 0.0) (=> (=> (and (<= 0.0 ts1uscore0) (<= ts1uscore0 t1uscore0)) (and (>= (+ (* amax ts1uscore0) v) 0.0) (<= (+ ts1uscore0 1) (+ ep 1)))) (<= (- (* ?v_0 ?v_0) ?v_1) (* ?v_2 (- M1uscore0 (* (/ 1.0 2.0) (+ (+ (* amax (* t1uscore0 t1uscore0)) (* (* 2.0 t1uscore0) v)) (* 2.0 Z1uscore0)))))))) (>= d 0.0)) (> b 0.0)) (> ep 0.0)) (> amax 0.0)) (>= v 0.0)) (>= SB (+ (/ (- (* v v) ?v_1) ?v_2) (* (+ (/ amax b) 1.0) (+ (* (/ amax 2.0) (* ep ep)) (* ep v)))))))))))
(check-sat)
(exit)
