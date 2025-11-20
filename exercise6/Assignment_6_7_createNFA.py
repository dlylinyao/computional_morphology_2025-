import hfst
tok = hfst.HfstTokenizer()
tok.add_multichar_symbol(hfst.EPSILON)

# Convert string to FST
def stringToFst(str):
    tokenized = tok.tokenize(str)
    fst = hfst.tokenized_fst(tokenized)
    return fst
  
# Create lexicon transducer from list of strings
def createLexicon(strings):
    lexicon = hfst.HfstTransducer()
    for string in strings:
        tr = stringToFst(string)
        lexicon.disjunct(tr)
    return lexicon

# Write a transdcuer to a file
def writeToFile(transducer, fileName):
    ostr = hfst.HfstOutputStream(filename=fileName)
    ostr.write(transducer)
    ostr.flush()
    ostr.close()

def main():   
    nounStems = ['kisko', 'kissa', 'koira', 'kori', 'koulu', 'taulu', 'tori', 'tuoksu']
    caseEndings = [hfst.EPSILON, 'a', 'lla', 'lle', 'lta', 'n']

    nounLexicon = createLexicon(nounStems)
    caseLexicon = createLexicon(caseEndings)


    writeToFile(nounLexicon, 'nouns.hfst')
    writeToFile(caseLexicon, 'cases.hfst')
    
    nounLexiconKleenePlus = hfst.HfstTransducer(nounLexicon)
    nounLexiconKleenePlus.repeat_plus();
    writeToFile(nounLexiconKleenePlus, 'nounsKleenePlus.hfst')
    
    nounsWithCases = hfst.HfstTransducer(nounLexiconKleenePlus)
    nounsWithCases.concatenate(caseLexicon)
    writeToFile(nounsWithCases, 'nounsKleenePlusWithCases.hfst')

    verbStems = ['kisko', 'tuoksu']
    verbEndings = [hfst.EPSILON, 'a', 'n', 't', 'mme', 'tte', 'vat']

    verbLexicon = createLexicon(verbStems)
    verbEndingLexicon = createLexicon(verbEndings)

    verbsWithEndings = hfst.HfstTransducer(verbLexicon)
    verbsWithEndings.concatenate(verbEndingLexicon)
    writeToFile(verbsWithEndings, 'verbsWithEndings.hfst')

    nounsAndVerbs = hfst.HfstTransducer(nounsWithCases)
    nounsAndVerbs.disjunct(verbsWithEndings)
    writeToFile(nounsAndVerbs, 'nounsAndVerbs.hfst')  # 这就是作业 a 要画的图

    nv_noeps = hfst.HfstTransducer(nounsAndVerbs)
    nv_noeps.remove_epsilons()
    writeToFile(nv_noeps, 'nounsAndVerbs_noeps.hfst')

    nv_noeps_det = hfst.HfstTransducer(nv_noeps)
    nv_noeps_det.determinize()
    writeToFile(nv_noeps_det, 'nounsAndVerbs_noeps_det.hfst')

    nv_noeps_det_min = hfst.HfstTransducer(nv_noeps_det)
    nv_noeps_det_min.minimize()
    writeToFile(nv_noeps_det_min, 'nounsAndVerbs_noeps_det_min.hfst')

    print("Created files:")
    print("  nouns.hfst")
    print("  cases.hfst")
    print("  nounsKleenePlus.hfst")
    print("  nounsKleenePlusWithCases.hfst")
    print("  verbsWithEndings.hfst")
    print("  nounsAndVerbs.hfst")
    print("  nounsAndVerbs_noeps.hfst")
    print("  nounsAndVerbs_noeps_det.hfst")
    print("  nounsAndVerbs_noeps_det_min.hfst")

main()