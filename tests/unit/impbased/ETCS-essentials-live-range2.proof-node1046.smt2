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

 KeYmaera example: ETCS-essentials-live-range2.proof, node 1046 For more info see: @see "Andre Platzer and Jan-David Quesel. European Train Control System: A case study in formal verification. In Karin Breitman and Ana Cavalcanti, editors, 11th International Conference on Formal Engineering Methods, ICFEM, Rio de Janeiro, Brasil, Proceedings, volume 5885 of LNCS, pages 246-265. Springer, 2009."
|)
(set-info :category "industrial")
(set-info :status sat)
(declare-fun t0uscore0 () Real)
(declare-fun zuscore1dollarskuscore0 () Real)
(declare-fun ts0uscore0 () Real)
(declare-fun zuscore1 () Real)
(declare-fun b () Real)
(declare-fun A () Real)
(declare-fun Auscore0uscore0dollarmvuscore0 () Real)
(declare-fun vuscore1dollarskuscore0 () Real)
(declare-fun vo () Real)
(declare-fun puscore0dollarskuscore2 () Real)
(declare-fun ep () Real)
(declare-fun vuscore1 () Real)
(declare-fun uscorenuscore0dollarskuscore0 () Real)
(assert (not (exists ((Auscore0uscore0dollarmvuscore0 Real)) (exists ((t0uscore0 Real)) (forall ((ts0uscore0 Real))
	(=>
		(and (and (and (and (and (and
			(> uscorenuscore0dollarskuscore0 0.0)
			(>= (+ zuscore1dollarskuscore0 (* (* uscorenuscore0dollarskuscore0 ep) vo)) puscore0dollarskuscore2))
			(= vuscore1dollarskuscore0 vo))
			(> vo 0.0))
			(> ep 0.0))
			(> b 0.0))
			(>= A 0.0))
		(and (and (and (and
			(>= t0uscore0 0.0)
			(=>
				(and
					(<= 0.0 ts0uscore0)
					(<= ts0uscore0 t0uscore0))
				(<= ts0uscore0 ep)))
			(>= (+ (* (/ 1.0 2.0) (+ (+ (* Auscore0uscore0dollarmvuscore0 (* t0uscore0 t0uscore0)) (* (* 2.0 t0uscore0) vuscore1)) (* 2.0 zuscore1))) (* (* ep vo) (+ (- 1.0) uscorenuscore0dollarskuscore0))) puscore0dollarskuscore2))
			(= (+ (* Auscore0uscore0dollarmvuscore0 t0uscore0) vuscore1) vo))
			(<= Auscore0uscore0dollarmvuscore0 A)
	)))))))
(check-sat)
(exit)
