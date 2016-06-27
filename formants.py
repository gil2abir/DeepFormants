
import extract_features as features
from subprocess import call
import sys
import argparse
import tempfile


def easy_call(command, debug_mode=True):
    try:
        if debug_mode:
            print >>sys.stderr, command
        call(command, shell=True)
    except Exception as exception:
        print "Error: could not execute the following"
        print ">>", command
        print type(exception)     # the exception instance
        print exception.args      # arguments stored in .args
        exit(-1)


def main(wav_filename, preds_filename, begin, end):
    tmp_features_filename = tempfile._get_default_tempdir() + "/" + next(tempfile._get_candidate_names()) + ".txt"
    print tmp_features_filename

    if begin > 0.0 or end > 0.0:
        features.create_features(wav_filename, tmp_features_filename, begin, end)
        easy_call("th load_estimation_model.lua " + tmp_features_filename + ' ' + preds_filename)
    else:
        features.create_features(wav_filename, tmp_features_filename)
        easy_call("th load_tracking_model.lua " + tmp_features_filename + ' ' + preds_filename)


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='Extract features for formants estimation.')
    parser.add_argument('wav_file', default='', help="WAV audio filename (single vowel or an whole utternace)")
    parser.add_argument('formants_file', default='', help="output formant text file")
    parser.add_argument('--begin', help="beginning time in the WAV file", default=0.0, type=float)
    parser.add_argument('--end', help="end time in the WAV file", default=-1.0, type=float)
    args = parser.parse_args()

    main(args.wav_file, args.formants_file, args.begin, args.end)

