// PEG
#define PEG_2_1 2
#define PEG_3_1 3
#define PEG_2_2 4
#define PEG_2_3 5
#define PEG_3_2 6
#define PEG_3_3 7
#define PEG_2_4 8
#define PEG_2_5 9
#define PEG_2_6 10
#define PEG_2_7 11
#define PEG_3_4 12
#define PEG_3_5 13
#define PEG_3_6 14
#define PEG_3_7 15

#define _JOIN(a,b) a ## b
#define JOIN(a,b) _JOIN(a,b)


#define PEG(a,b) JOIN(JOIN(PEG_,a),JOIN(_,b))

#define IDX 0
#define JUST 1

// :: a -> a
// *[a ID] -> a
#define ID [IDX 1]

// :: [a b] -> a
// *[[a b] CAR] -> a
#define CAR [IDX 2]

// :: [a b] -> b
// *[[a b] CDR] -> b
#define CDR [IDX 3]

// a -> ?a
#define WUT [3 ID]

// a -> +a
#define LUS [4 ID]

// [a b] -> =[a b]
#define TIS [5 ID]
#define TIS2(a,b) [5 a b]

// :: [[a -> b] [b -> c]] -> [a -> c]
// *[a *[[f g] COMPOSE]] -> *[*[a f] g]
#define COMPOSE [[JUST 7] ID]

// :: [a ([a b] -> c)] -> (a -> c)
// *[a *[[b f] PARTIAL]] -> *[[b a] f]
#define PARTIAL [[JUST 8] [[JUST JUST] CAR] CDR]

// :: (a -> a) -> a
// *[f FIX] -> *[f f]
#define FIX [2 ID ID]

// Helper functions
// *[a REDUCE(f)] -> *[a *f]
#define REDUCE(f,b) [2 ID 7 [JUST b] f]
// *[a COMPOSE2(f,g)] -> *[*[a f] g]
#define COMPOSE [7 f g]

#define LUS1(f) [4 f]

#define PUSH(b,g) [8 [JUST b] g]

#define ARG(i) [IDX PEG(3,i)]
#define CALL(func) [9 PEG(2,LIB ## func) ID]

#define ADDR [6 TIS2(ARG(2),ARG(7)) ARG(6) COMPOSE2([CAR LUS1(ARG(2)) LUS1(ARG(6)) ARG(7)], CALL(_ADDR))]
// #define MULR [6 COMPOSE2([ARG(4) ARG(7)],TIS) ARG(5) COMPOSE2([CAR LUS1(ARG(2)) COMPOSE2([CAR [JUST 0] ARG(5) ARG(6)], CALL(_ADDR))] ARG(6) ARG(7)], CALL(_MULR))]
// #define DIVR [6 COMPOSE2([ARG(5) ARG(7)],TIS) ARG(4) COMPOSE2([CAR LUS1(ARG(2)) COMPOSE2([CAR [JUST 0] ARG(5) ARG(6)], CALL(_ADDR))] ARG(6) ARG(7)], CALL(_DIVR))]

#define LIB ADDR
#define LIB_ADDR 1
// #define LIB_MULR 10
// #define LIB_DIVR 11
PUSH(0,PUSH(LIB,CALL(_ADDR)))

