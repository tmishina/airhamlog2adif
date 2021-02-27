from datetime import datetime
from datetime import timezone
import csv
import sys
import argparse

freq2lambda = {'430MHz': '70CM'}


def main(config):
    csv_file = open(config['csv_filepath'])
    f = csv.DictReader(csv_file,
                       delimiter=",",
                       doublequote=True,
                       lineterminator="\r\n",
                       quotechar='"',
                       skipinitialspace=True)

    for row in f:
        callsign = row['callsign']
        sent_qth = row['sent_qth']
        if ':' in sent_qth:
            qth_number = sent_qth.split(':')[0] + '_' + sent_qth.split(
                ':')[1].split(' ')[-1]
        else:
            qth_number = sent_qth
        with open(f"{config['output_prefix']}export_{qth_number}.adi",
                  'a') as f:
            if len(row['portable']) > 0:
                callsign += '/' + row['portable']
            print(f"<CALL:{len(callsign)}>{callsign}", file=f)
            ts = datetime.strptime(
                row['qso_at'],
                '%Y-%m-%d %H:%M:%S %z')  # '2020-12-12 16:51:00 +0900'
            ts_utc = ts.astimezone(timezone.utc)
            ts_date = ts_utc.strftime('%Y%m%d')
            ts_time = ts_utc.strftime('%H%M')
            print(f"<QSO_DATE:{len(ts_date)}:D>{ts_date}", file=f)
            print(f"<TIME_ON:{len(ts_time)}>{ts_time}", file=f)
            freq = freq2lambda[row['frequency']]
            print(f"<BAND:{len(freq)}>{freq}", file=f)
            print(f"<MODE:{len(row['mode'])}>{row['mode']}", file=f)
            print(f"<RST_SENT:{len(row['sent_rst'])}>{row['sent_rst']}",
                  file=f)
            print(
                f"<RST_RCVD:{len(row['received_rst'])}>{row['received_rst']}",
                file=f)
            print(f"<QTH:{len(row['received_qth'])}>{row['received_qth']}",
                  file=f)
            print(f"<NAME:{len(row['received_qra'])}>{row['received_qra']}",
                  file=f)
            print(f"<COMMENT:{len(row['remarks'])}>{row['remarks']}", file=f)
            qsl_sent = 'Y' if row['is_qsl_sent'] == 'true' else 'N'
            print(f"<QSL_SENT:{len(qsl_sent)}>{qsl_sent}", file=f)
            if 'tx_pwr' in config:
                print(f"<TX_PWR:{len(config['tx_pwr'])}>{config['tx_pwr']}",
                      file=f)
            print('<EOR>', file=f)
            print('', file=f)

    return 0


def cli():
    parser = argparse.ArgumentParser(
        description='Airhamlog CSV to ADIF Converter')
    parser.add_argument('csv_filepath')
    parser.add_argument('--tx-pwr', default='5')
    parser.add_argument('-o',
                        '--output-prefix',
                        help='filename prefix for output ADIF files',
                        default='export_')
    args = parser.parse_args()
    return main(vars(args))


if __name__ == '__main__':
    sys.exit(cli())
