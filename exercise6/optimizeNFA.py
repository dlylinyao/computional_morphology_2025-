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

    noeps = hfst.HfstTransducer(nounsWithCases)
    noeps.remove_epsilons()
    writeToFile(noeps, 'nouns_noeps.hfst')

    noeps_det = hfst.HfstTransducer(noeps)
    noeps_det.determinize()
    writeToFile(noeps_det, 'nouns_noeps_det.hfst')

    noeps_det_min = hfst.HfstTransducer(noeps_det)
    noeps_det_min.minimize()
    writeToFile(noeps_det_min, 'nouns_noeps_det_min.hfst')

    print("All FSTs created successfully:")
    print(" - nouns.hfst")
    print(" - cases.hfst")
    print(" - nounsKleenePlus.hfst")
    print(" - nounsKleenePlusWithCases.hfst")
    print(" - nouns_noeps.hfst")
    print(" - nouns_noeps_det.hfst")
    print(" - nouns_noeps_det_min.hfst")


main()