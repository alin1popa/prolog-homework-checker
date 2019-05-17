from os import listdir
from os.path import isdir, join
from subprocess import call, check_output
import subprocess
import sys
import argparse
import json
import os

# prolog goals
checkingScript = '\
    retea(R),\
    from(F),\
    to(T),\
    stp(R,Root,Edges),\
    write(Root), write(:), write(Edges), halt\
';
checkingScriptWithBonus = '\
    retea(R),\
    from(F),\
    to(T),\
    drum(R, F, T, Root, Edges, Path),\
    write(Root), write(:), write(Edges), write(:), write(Path), halt\
';


# grading
PERCENTAGE_ROOT = 0.10
PERCENTAGE_EDGES = 0.90
PERCENTAGE_BONUS = 0.25
NO_EASY_TESTS = 1
NO_HARD_TESTS = 0
EASY_TESTS_SCORE = 0.25
HARD_TESTS_SCORE = 0.65


def generate_output(swipl, tema, testin, goal, suppress_errors):
    # open test file
    with open(testin) as f:
        content = f.readlines()
        
    # remove endline characters
    content = [x.strip() for x in content] 
    
    # build prolog asserts
    for index in range(len(content)):
        line = content[index]
        assertline = 'assert(({0}))'.format(line[:-1])
        content[index] = assertline
        
    # concatenate assertions
    assertions = ','.join(content);
    
    # final prolog script
    prolog = assertions + ',' + goal + '.';
        
    # run for 10 seconds max
    #command = 'timeout 10 {0} -t halt -l "{1}" -g "{2}"'.format(swipl, tema, prolog)
    command = '{0} -t halt -l "{1}" -g "{2}"'.format(swipl, tema, prolog)
    
    try:
        if not suppress_errors:
            r = check_output(command, shell=True)
        else:
            with open(os.devnull, 'w') as devnull:
                r = check_output(command, shell=True, stderr=devnull)
    except subprocess.CalledProcessError as grepexc:
        # return code 1 means goal failed
        # return code 2 means raised exception
        r = "false" if grepexc.returncode is 1 else "error"
    return r.decode("utf-8") if r else "false"

    
def run_test(swipl, hwfile, testfile, reffile, suppress_errors = False):
    output = generate_output(swipl, hwfile, testfile, checkingScript, suppress_errors)
    
    outparts = output.split(':')
    outroot = json.loads(outparts[0])
    outedges = json.loads(outparts[1])
    
    with open(reffile, 'r') as file:
        reffile = file.read().replace('\n', '')
    
    refparts = reffile.split(':')
    refroot = json.loads(refparts[0])
    refedges = json.loads(refparts[1])
    refpath = json.loads(refparts[2])
    
    score = 0
    if outroot == refroot:
        score += PERCENTAGE_ROOT
        if sorted(outedges) == sorted(refedges):
            score += PERCENTAGE_EDGES
            
            output = generate_output(swipl, hwfile, testfile, checkingScriptWithBonus, suppress_errors)
            outparts = output.split(':')
            outpath = json.loads(outparts[2])
            if outpath == refpath:
                score += PERCENTAGE_BONUS
    
    return output, score
   
 
def run_all(swipl, hwfile):
    score_per_easy_test = EASY_TESTS_SCORE / NO_EASY_TESTS
    #score_per_hard_test = HARD_TESTS_SCORE / NO_HARD_TESTS
    
    print("Type #no\tresult%\tpoints\ttotal")
    
    total = 0
    for i in range(NO_EASY_TESTS):
        testfile = "easy/in_easy" + str(i) + ".txt"
        reffile = "easy/out_easy" + str(i) + ".txt"
        
        output, score = run_test(swipl, hwfile, testfile, reffile, True)
        
        points = score * score_per_easy_test
        total += points
        
        print("Easy #{0}:\t{1}%\t{2}\t{3}".format(i, score*100, points*100, total*100))
 
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prolog Homework Checker')
    parser.add_argument('--swiplexe', default='swipl',
                    help='Absolute or relative path to swipl.exe; default \
                    "swipl" but you need to add its location to PATH')
    parser.add_argument('--hwfile', required=True,
                    help='Path to prolog homework file. Example: main.pl')
    parser.add_argument('--testfile',
                    help='Path to test file. Example: easy/in_easy1.txt')
    parser.add_argument('--reffile',
                    help='Path to reference file. Example: easy/out_easy1.txt')
    args = parser.parse_args()
    
    if (args.testfile and not args.reffile) or (args.reffile and not args.testfile):
        sys.exit('If you don\'t run all tests you must specify both --testfile and --reffile parameters')
    
    if args.testfile and args.reffile:
        output, score = run_test(args.swiplexe, args.hwfile, args.testfile, args.reffile)
        print("Your score on this test: {0}%".format(score*100))
        with open('output.txt', 'w') as f:
            f.write(output)
    else:
        run_all(args.swiplexe, args.hwfile)
        
