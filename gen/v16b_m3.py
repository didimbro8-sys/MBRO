import sys; sys.path.insert(0,"/tmp/claude-0/-home-claude/45fbbbb6-d482-5788-aa3b-b4a14b8c49ad/scratchpad/gen")
import motion3 as M
S=M.S
V={
"AM-Digital_16oct_0700_mot-du-fondateur_v3":[
 {"dur":2.6,"label":"Le mot du fondateur","title":"Pourquoi *AM.Digital* revient ?","size":104},
 {"dur":2.6,"label":"Le constat","title":"Trop d'entreprises publient *beaucoup*…","size":96},
 {"dur":2.4,"title":"…et vendent *peu*.","size":150},
 {"dur":2.8,"big":"30","bigSize":400,"title":"jours pour *changer* ça","size":96},
 {"dur":3.0,"label":"Chaque jour, gratuitement","title":"7h · 12h · *18h*","size":110,"sub":"Des conseils concrets pour faire vendre votre entreprise en ligne."},
 {"dur":3.0,"label":"Rejoignez-nous","title":"On *commence* maintenant","size":110,"cta":"Abonnez-vous"}],
"AM-Digital_16oct_1800_diagnostic_v3":[
 {"dur":2.6,"label":"Notre méthode","title":"Le *diagnostic* digital","size":124},
 {"dur":2.8,"big":"2","bigSize":420,"title":"semaines pour tout *analyser*","size":92,"sub":"Réseaux sociaux, site, supports."},
 {"dur":2.8,"big":"5","bigSize":420,"title":"*priorités* claires, pas plus","size":92},
 {"dur":3.0,"num":"✓","label":"Résultat","title":"Un *plan* d'action","size":120,"sub":"Quoi faire, dans quel ordre, avec quels moyens."},
 {"dur":3.4,"label":"Pour commencer","title":"Écrivez *DIAGNOSTIC*","size":104,"sub":"Sur WhatsApp : +225 01 71 95 45 23","cta":"Écrivez-nous"}],
}
k=sys.argv[1]; print(M.build(V[k], f"{S}/medias/{k}.mp4", seed=3 if "diag" in k else 1))
