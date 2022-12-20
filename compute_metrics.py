from argparse import ArgumentParser, RawTextHelpFormatter
from numpy import linspace
from matplotlib.pyplot import subplots, savefig

sigma_range = list(linspace(0, 1, 1001))


def populate_metric_dicts(lines, col_idx, accuracy_dict, length_dict, distance=True):

    for sigma in sigma_range:
        accuracy_dict[sigma] = 0
        length_dict[sigma] = 0

    total_reads = 0
    total_length = 0

    for i, line in enumerate(lines):
        if i == 0:
            continue
        values = line.strip().split(',')
        edit_distance = float(values[col_idx])
        read_len = float(values[-1])
        truth_len = float(values[-2])

        used_len = read_len if col_idx == 2 else truth_len
        total_reads += 1
        total_length += read_len
        for sigma in sigma_range:
            if used_len > 0:
                if distance:
                    if edit_distance / used_len <= sigma:
                        accuracy_dict[sigma] += 1
                        length_dict[sigma] += read_len
                else:
                    if edit_distance / used_len >= sigma:
                        accuracy_dict[sigma] += 1
                        length_dict[sigma] += read_len

    # converting counts to percentages
    for sigma in sigma_range:
        accuracy_dict[sigma] = float(accuracy_dict[sigma]) / total_reads * 100
        length_dict[sigma] = float(length_dict[sigma]) / total_length * 100


def compute_metrics(args):

    # Metrics
    metrics = dict()
    for aligner, csv in zip(args.summaries_names, args.summaries):

        metrics[aligner] = {
            'overlap': {
                'accuracy': dict(),
                'length': dict()
            },
            'truth': {
                'accuracy': dict(),
                'length': dict()
            },
            'read': {
                'accuracy': dict(),
                'length': dict()
            }
        }

        lines = open(csv).read().split('\n')[:-1]
        populate_metric_dicts(
            lines, 4, metrics[aligner]['overlap']['accuracy'], metrics[aligner]['overlap']['length'], distance=False
        )
        populate_metric_dicts(lines, 3, metrics[aligner]['truth']['accuracy'], metrics[aligner]['truth']['length'])
        populate_metric_dicts(lines, 2, metrics[aligner]['read']['accuracy'], metrics[aligner]['read']['length'])

    # Plot accuracy
    fig, (overlap, truth, read) = subplots(3, 1)

    overlap.set_xlabel('Overlap criterion ($\delta$)')
    overlap.set_ylabel('% Correctly aligned')
    truth.set_xlabel('Edit distance criterion ($\sigma_{truth}$)')
    truth.set_ylabel('% Correctly aligned')
    read.set_xlabel('Edit distance criterion ($\sigma_{read}$)')
    read.set_ylabel('% Correctly aligned')

    for aligner in args.summaries_names:
        overlap.plot(sigma_range, metrics[aligner]['overlap']['accuracy'].values(), label=aligner)
        truth.plot(sigma_range, metrics[aligner]['truth']['accuracy'].values(), label=aligner)
        read.plot(sigma_range, metrics[aligner]['read']['accuracy'].values(), label=aligner)

    overlap.grid()
    overlap.legend()
    truth.grid()
    truth.legend()
    read.grid()
    read.legend()


    fig.set_figwidth(3.87)
    fig.set_figheight(11.5)
    fig.tight_layout(pad=1.15)

    savefig(f'{args.output_name}_accuracy.pdf')

    # Plot length
    fig, (overlap, truth, read) = subplots(3, 1)

    overlap.set_xlabel('Overlap criterion ($\delta$)')
    overlap.set_ylabel('% Good length')
    truth.set_xlabel('Edit distance criterion ($\sigma_{truth}$)')
    truth.set_ylabel('% Good length')
    read.set_xlabel('Edit distance criterion ($\sigma_{read}$)')
    read.set_ylabel('% Good length')

    for aligner in args.summaries_names:
        overlap.plot(sigma_range, metrics[aligner]['overlap']['length'].values(), label=aligner)
        truth.plot(sigma_range, metrics[aligner]['truth']['length'].values(), label=aligner)
        read.plot(sigma_range, metrics[aligner]['read']['length'].values(), label=aligner)

    overlap.grid()
    overlap.legend()
    truth.grid()
    truth.legend()
    read.grid()
    read.legend()

    fig.set_figwidth(3.87)
    fig.set_figheight(11.5)
    fig.tight_layout(pad=1.15)

    savefig(f'{args.output_name}_length.pdf')


if __name__ == '__main__':

    parser = ArgumentParser(
        description='''
               Computes distance and overlap metrics based on summary files.
               Outputs plots and tables.            
            ''',
        formatter_class=RawTextHelpFormatter
    )

    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('-n', '--output-name', type=str, help='Output base name', required=True)
    requiredNamed.add_argument(
        '-s', '--summaries', type=str,
        help='Input summary (csv( files used to compute metrics, one per aligner/configuration',
        required=True, nargs='+'
    )
    requiredNamed.add_argument(
        '-sn', '--summaries-names', type=str, help='Name of aligners/configurations, used in plot/table legends',
        required=True, nargs='+'
    )

    compute_metrics(parser.parse_args())
