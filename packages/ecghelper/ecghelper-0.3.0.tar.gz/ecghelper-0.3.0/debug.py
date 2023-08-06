import os
import numpy as np
from pathlib import Path

from ecghelper.waveform import WaveformRecord

def test_write():
    # inputs
    data_path = Path('tests/data').resolve()
    filename = '82000'

    # read in the record
    record = WaveformRecord.from_xml(data_path / f"{filename}.xml")

    fcns = [
        (".xml", record.to_xml, WaveformRecord.from_xml),
        (".hea", record.to_wfdb, WaveformRecord.from_wfdb),
        # TODO: edf is failing!
        # (".edf", record.to_edf, WaveformRecord.from_edf),
        (".csv",record.to_csv, WaveformRecord.from_csv),
    ]
    # test fcn
    for ext, to_fcn, load_fcn in fcns:
        # EDF precision is 8 chars
        signal = np.around(record.data, 5)
        output_file = Path(f'{filename}{ext}')
        to_fcn(output_file)
        assert os.path.exists(output_file)

        # re-load, compare to original signal
        record_reloaded = load_fcn(output_file)
        signal_reloaded = record_reloaded.data
        assert signal_reloaded.shape == signal.shape

        # assert approximately equal
        assert (abs(signal_reloaded - signal) < 0.01).all()

        assert signal_reloaded.shape[0] > 0
        assert signal_reloaded.shape[1] == 8

        # units should be between -2 and 5 millivolts
        assert signal_reloaded.min() > -2
        assert signal_reloaded.max() < 5

def test_read():
    # inputs
    data_path = Path('tests/data').resolve()
    fcns = [
        (".xml", WaveformRecord.from_xml),
        (".hea", WaveformRecord.from_wfdb),
        (".edf", WaveformRecord.from_edf),
        # (".csv", WaveformRecord.from_csv),
    ]
    filename = '82000'

    # test fcn
    for ext, load_fcn in fcns:
        record = load_fcn(data_path / f"{filename}{ext}")
        assert record.data.shape[0] > 0
        assert record.data.shape[1] == 8

        # units should be between -2 and 5 millivolts
        assert record.data.min() > -2
        assert record.data.max() < 5

def main():
    test_write()

if __name__ == '__main__':
    main()