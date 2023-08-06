# Licensed under a 3-clause BSD style license - see LICENSE.rst

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass  # package is not installed

import datetime as dt
import glob
import itertools
import os
import re
import sunpy
import urllib.request
import warnings
from pathlib import Path

import cdflib
import numpy as np
import pandas as pd
from astropy.io.votable import parse_single_table
if int(sunpy.__version__[0]) == 4:
    from sunpy.io.cdf import read_cdf
elif int(sunpy.__version__[0]) >= 5:
    from sunpy.io._cdf import read_cdf
from sunpy.timeseries import TimeSeries

# omit Pandas' PerformanceWarning
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


"""
Example code that loads low latency (ll) electron and proton (+alphas) fluxes
(and errors) for 'ept' 'north' telescope from Apr 15 2021 to Apr 16 2021 into
two Pandas dataframes (one for protons & alphas, one for electrons). In general
available are 'sun', 'asun', 'north', and 'south' viewing directions for 'ept'
and 'het' telescopes of SolO/EPD.

from epd_loader import *

df_protons, df_electrons, energies = \
_read_epd_cdf('ept', 'north', 'll', 20210415, 20210416,
path='/home/userxyz/solo/data/')

# plot protons and alphas
ax = df_protons.plot(logy=True, subplots=True, figsize=(20,60))
plt.show()

# plot electrons
ax = df_electrons.plot(logy=True, subplots=True, figsize=(20,60))
plt.show()
"""

"""
Example code that loads level 2 (l2) electron and proton (+alphas) fluxes
(and errors) for 'het' 'sun' telescope from Aug 20 2020 to Aug 20 2020 into
two Pandas dataframes (one for protons & alphas, one for electrons).

from epd_loader import *

df_protons, df_electrons, energies = \
_read_epd_cdf('het', 'sun', 'l2', 20200820, 20200821,
path='/home/userxyz/solo/data/')

# plot protons and alphas
ax = df_protons.plot(logy=True, subplots=True, figsize=(20,60))
plt.show()

# plot electrons
ax = df_electrons.plot(logy=True, subplots=True, figsize=(20,60))
plt.show()

"""


def _check_duplicates(filelist, verbose=True):
    """
    Checks for duplicate file entries in filelist (that are only different by
    version number). Returns filelist with duplicates removed.
    """
    for _, g in itertools.groupby(filelist, lambda f: f.split('_')[:-1]):
        dups = list(g)
        if len(dups) > 1:
            dups.sort()
            if verbose:
                print('')
                print('WARNING: Following data files are duplicates with ' +
                      'different version numbers:')
            for i in dups:
                print(i)
            if verbose:
                print('')
                print('Removing following files from list that will be read: ')
            for n in range(len(dups)-1):
                print(dups[n])
                filelist.remove(dups[n])
            if verbose:
                print('You might want to delete these files in order to get ' +
                      'rid of this message.')
    return filelist


def _get_filename_url(cd):
    """
    Get download filename for a url from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0][1:-1]


def _load_tqdm(verbose=True):
    """
    Tries to load tqdm package for displaying download progress.
    Return True or False, depending of success state.
    If not available, returns False.
    """
    try:
        from tqdm import tqdm

        class DownloadProgressBar(tqdm):
            def update_to(self, b=1, bsize=1, tsize=None):
                if tsize is not None:
                    self.total = tsize
                self.update(b * bsize - self.n)

        def download_url(url, output_path):
            with DownloadProgressBar(unit='B', unit_scale=True, miniters=1,
                                     desc=output_path.split('/')[-1]) as t:
                urllib.request.urlretrieve(url, filename=output_path,
                                           reporthook=t.update_to)
        tqdm_available = True
    except ModuleNotFoundError:
        if verbose:
            print("Module tqdm not installed, won't show progress bar. To get rid of this: pip install tqdm")
        tqdm_available = False
        download_url = None
    return tqdm_available, download_url


def _get_epd_filelist(sensor, level, startdate, enddate, path,
                      filenames_only=False):
    """
    INPUT:
        sensor: 'ept' or 'het'
        level: 'll', 'l2'
        startdate, enddate: YYYYMMDD
        path: directory in which the data is located;
              e.g. '/home/userxyz/uni/solo/data/l2/epd/ept/'
        filenames_only: if True only give the filenames, not the full path
    RETURNS:
        Dictionary with four entries for 'sun', 'asun', 'north', 'south';
        each containing a list of files matching selection criteria.
    """

    if level == 'll':
        l_str = 'LL02'
        t_str = 'T??????-????????T??????'
    if level == 'l2':
        l_str = 'L2'
        t_str = ''

    filelist_sun = []
    filelist_asun = []
    filelist_north = []
    filelist_south = []
    for i in range(startdate, enddate+1):
        filelist_sun = filelist_sun + \
            glob.glob(path+'solo_'+l_str+'_epd-'+sensor+'-sun-rates_' +
                      str(i) + t_str + '_V*.cdf')
        filelist_asun = filelist_asun + \
            glob.glob(path+'solo_'+l_str+'_epd-'+sensor+'-asun-rates_' +
                      str(i) + t_str + '_V*.cdf')
        filelist_north = filelist_north + \
            glob.glob(path+'solo_'+l_str+'_epd-'+sensor+'-north-rates_' +
                      str(i) + t_str + '_V*.cdf')
        filelist_south = filelist_south + \
            glob.glob(path+'solo_'+l_str+'_epd-'+sensor+'-south-rates_' +
                      str(i) + t_str + '_V*.cdf')

    if filenames_only:
        filelist_sun = [os.path.basename(x) for x in filelist_sun]
        filelist_asun = [os.path.basename(x) for x in filelist_asun]
        filelist_north = [os.path.basename(x) for x in filelist_north]
        filelist_south = [os.path.basename(x) for x in filelist_south]

    filelist = {'sun': filelist_sun,
                'asun': filelist_asun,
                'north': filelist_north,
                'south': filelist_south
                }
    return filelist


def _get_step_filelist(level, startdate, enddate, path,
                       filenames_only=False):
    """
    INPUT:
        level: 'll', 'l2'
        startdate, enddate: YYYYMMDD
        path: directory in which the data is located;
              e.g. '/home/userxyz/uni/solo/data/l2/epd/step/'
        filenames_only: if True only give the filenames, not the full path
    RETURNS:
        List of files matching selection criteria.
    """

    sensor = 'step'

    if level == 'll':
        l_str = 'LL02'
        t_str = 'T??????-????????T??????'
    if level == 'l2':
        l_str = 'L2'
        t_str = ''

    if startdate <= 20211022:
        product = 'rates'
    if startdate > 20211022:
        product = 'main'

    filelist = []
    for i in range(startdate, enddate+1):
        filelist = filelist + \
            glob.glob(path+'solo_'+l_str+'_epd-'+sensor+'-'+product+'_' +
                      str(i) + t_str + '_V*.cdf')

    if filenames_only:
        filelist = [os.path.basename(x) for x in filelist]

    return filelist


def _epd_ll_download(date, path, sensor, viewing=None):
    """
    Download EPD low latency data from http://soar.esac.esa.int/soar
    One file/day per call.

    Note: for sensor 'step' the 'viewing' parameter is necessary, but it

    Example:
        _epd_ll_download(20210415,
                        '/home/userxyz/solo/data/low_latency/epd/ept/',
                        'ept', 'north')
        _epd_ll_download(20200820,
                        '/home/userxyz/solo/data/low_latency/epd/step/',
                        'step')
    """

    # try loading tqdm for download progress display
    tqdm_available, download_url = _load_tqdm(verbose=True)

    # get list of available data files, obtain corresponding start & end time
    fl = get_available_soar_files(date, date, sensor, 'll')
    # try:
    if sensor.lower() == 'step':
        stime = 'T'+fl[0].split('T')[1].split('-')[0]
        etime = 'T'+fl[0].split('T')[2].split('_')[0]
        url = 'http://soar.esac.esa.int/soar-sl-tap/data?' + \
            'retrieval_type=LAST_PRODUCT&data_item_id=solo_LL02_epd-' + \
            sensor.lower()+'-rates_'+str(date) + \
            stime+'-'+str(date+1)+etime+'&product_type=LOW_LATENCY'
    else:
        stime = 'T'+fl[0].split('T')[1].split('-')[0]  # fl[0][-32:-25]
        etime = 'T'+fl[0].split('T')[2].split('_')[0]  # fl[0][-16:-9]
        url = 'http://soar.esac.esa.int/soar-sl-tap/data?' + \
            'retrieval_type=LAST_PRODUCT&data_item_id=solo_LL02_epd-' + \
            sensor.lower()+'-'+viewing.lower()+'-rates_'+str(date) + \
            stime+'-'+str(date+1)+etime+'&product_type=LOW_LATENCY'

    # Get filename from url
    file_name = _get_filename_url(
        urllib.request.urlopen(url).headers['Content-Disposition'])

    if tqdm_available:
        download_url(url, path+file_name)
    else:
        urllib.request.urlretrieve(url, path+file_name)

    return path+file_name


def _epd_l2_download(date, path, sensor, viewing=None):
    """
    Download EPD level 2 data from http://soar.esac.esa.int/soar
    One file/day per call.

    Example:
        _epd_l2_download(20200820,
                        '/home/userxyz/solo/data/l2/epd/ept/',
                        'ept', 'north')
        _epd_l2_download(20200820,
                        '/home/userxyz/solo/data/l2/epd/step/',
                        'step')
    """

    # try loading tqdm for download progress display
    tqdm_available, download_url = _load_tqdm(verbose=True)

    if sensor.lower() == 'step':
        if date <= 20211022:
            product = 'rates'
        if date > 20211022:
            product = 'main'
        url = 'http://soar.esac.esa.int/soar-sl-tap/data?' + \
              'retrieval_type=LAST_PRODUCT&data_item_id=solo_L2_epd-' + \
              sensor.lower()+'-'+product+'_'+str(date) + \
              '&product_type=SCIENCE'
    else:
        url = 'http://soar.esac.esa.int/soar-sl-tap/data?' + \
            'retrieval_type=LAST_PRODUCT&data_item_id=solo_L2_epd-' + \
            sensor.lower()+'-'+viewing.lower()+'-rates_'+str(date) + \
            '&product_type=SCIENCE'

    # Get filename from url
    file_name = _get_filename_url(
        urllib.request.urlopen(url).headers['Content-Disposition'])

    if tqdm_available:
        download_url(url, path+file_name)
    else:
        urllib.request.urlretrieve(url, path+file_name)

    return path+file_name


def get_available_soar_files(startdate, enddate, sensor, level='l2'):
    """
    Get list of files available at SOAR

    Check ESA's SOAR database for available Solar Orbiter/EPD files in date
    range for give sensor and data level. Returns list of file names.

    Parameters
    ----------
    startdate : yyyymmdd (int)
        Provides year (yyyy), month (mm) and day (dd) of the start date as one
        combined integer; fill empty positions with zeros, e.g. '20210415'
    enddate : yyyymmdd (int)
        Provides year (yyyy), month (mm) and day (dd) of the end date as one
        combined integer; fill empty positions with zeros, e.g. '20210415'
    sensor : {'ept', 'het', 'step'}
        Defines EPD sensor
    level : {'l2', 'll'}, optional
        Defines level of data product: level 2 ('l2') or low-latency ('ll');
        by default 'l2'

    Returns
    -------
    filelist : list of str
        List of corresponding files available at SOAR.
    """

    # add 1 day to enddate to better work with SOAR's API
    # enddate = (pd.to_datetime(str(enddate))+
    #            pd.to_timedelta('1d')).strftime('%Y%m%d')

    sy = str(startdate)[0:4]
    sm = str(startdate)[4:6]
    sd = str(startdate)[6:8]

    ey = str(enddate)[0:4]
    em = str(enddate)[4:6]
    ed = str(enddate)[6:8]

    if level.lower() == 'l2':
        p_level = 'L2'  # "processing_level"
    #     data_type = 'v_sc_data_item'
    if level.lower() == 'll':
        p_level = 'LL02'  # "processing_level"
    #     data_type = 'v_ll_data_item'
    data_type = 'v_public_files'

    url = "http://soar.esac.esa.int/soar-sl-tap/tap/sync?REQUEST=doQuery&" + \
          "LANG=ADQL&retrieval_type=LAST_PRODUCT&FORMAT=votable_plain&" + \
          "QUERY=SELECT+*+FROM+"+data_type + \
          "+WHERE+(instrument='EPD')+AND+((begin_time%3E%3D'"+sy+"-"+sm + \
          "-"+sd+"+00:00:00')+AND+(begin_time%3C%3D'"+ey+"-"+em+"-"+ed + \
          "+01:00:00'))"

    filelist = urllib.request.urlretrieve(url)

    # open VO table, convert to astropy table, convert to pandas dataframe
    df = parse_single_table(filelist[0]).to_table().to_pandas()

    # convert bytestrings to unicode, from stackoverflow.com/a/67051068/2336056
    for col, dtype in df.dtypes.items():
        if dtype == object:  # Only process object columns.
            # decode, or return original value if decode return Nan
            df[col] = df[col].str.decode('utf-8').fillna(df[col])

    # remove duplicates with older version number
    df = df.sort_values('file_name')
    df.drop_duplicates(subset=['item_id'], keep='last', inplace=True)

    # only use data level wanted; i.e., 'LL' or 'L2'
    df = df[df['processing_level'] == p_level]

    # list filenames for given telescope (e.g., 'HET')
    # filelist = df['filename'][df['sensor'] == sensor.upper()].sort_values()
    filelist = [s for s in df['file_name'].values if sensor.lower() in s]

    if sensor.lower() == 'step' and startdate > 20211022:
        # list filenames for 'main' type (i.e., remove 'hcad')
        filelist = [s for s in filelist if "main" in s]
    else:
        # list filenames for 'rates' type (i.e., remove 'hcad')
        filelist = [s for s in filelist if "rates" in s]

    # filelist.sort()
    if len(filelist) == 0:
        print('No corresponding data found at SOAR!')
    return filelist


def _autodownload_cdf(startdate, enddate, sensor, level, path):
    """
    Uses get_available_soar_files() to check which files for selection criteria
    are available online. Compares with locally available files at 'path', and
    downloads missing files to 'path' using epd_l*_download()
    """
    fls = get_available_soar_files(startdate, enddate, sensor, level)
    for i in fls:
        my_file = Path(path)/i
        if not my_file.is_file():
            if os.path.exists(path) is False:
                print(f'Creating dir {path}')
                os.makedirs(path)
            tdate = int(i.split('_')[3].split('T')[0])
            tview = i.split('-')[2]
            if level.lower() == 'll':
                _ = _epd_ll_download(date=tdate, path=path, sensor=sensor,
                                     viewing=tview)
            if level.lower() == 'l2':
                _ = _epd_l2_download(date=tdate, path=path, sensor=sensor,
                                     viewing=tview)
    return


def epd_load(sensor, startdate, enddate=None, level='l2', viewing=None, path=None,
             autodownload=False, only_averages=False):
    """
    Load SolO/EPD data

    Load-in data for Solar Orbiter/EPD energetic charged particle sensors EPT,
    HET, and STEP. Supports level 2 and low latency data provided by ESA's
    Solar Orbiter Archive. Optionally downloads missing data directly. Returns
    data as Pandas dataframe.

    Parameters
    ----------
    sensor : {'ept', 'het', 'step'}
        Defines EPD sensor
    startdate : (datetime or int)
        Provides start date. Either a datetime object (e.g., dt.date(2021,12,31)
        or dt.datetime(2021,4,15)). Or a combined integer yyyymmdd with year
        (yyyy), month (mm) and day (dd) with empty positions filled with zeros,
        e.g. 20210415
    enddate : (datetime or int), optional
        Provides end date. Either a datetime object (e.g., dt.date(2021,12,31)
        or dt.datetime(2021,4,15)). Or a combined integer yyyymmdd with year
        (yyyy), month (mm) and day (dd) with empty positions filled with zeros,
        e.g. 20210415
        (if no enddate is given, 'enddate = startdate' will be set)
    level : {'l2', 'll'}, optional
        Defines level of data product: level 2 ('l2') or low-latency ('ll'). By
        default 'l2'
    viewing : {'sun', 'asun', 'north', 'south' or None}, optional
        Viewing direction of sensor. Required for 'ept' or 'het'; for 'step'
        should be None. By default None
    path : str, optional
        User-specified directory in which Solar Orbiter data is/should be
        organized; e.g. '/home/userxyz/solo/data/', by default None
    autodownload : bool, optional
        If True, will try to download missing data files from SOAR, by default
        False.
    only_averages : bool, optional
        If True, will for STEP only return the averaged fluxes, and not the data
        of each of the 15 Pixels. This will reduce the memory consumption. By
        default False.

    Returns
    -------
    For EPT & HET:
        1. Pandas dataframe with proton fluxes and errors (for EPT also alpha particles) in 'particles / (s cm^2 sr MeV)'
        2. Pandas dataframe with electron fluxes and errors in 'particles / (s cm^2 sr MeV)'
        3. Dictionary with energy information for all particles:
            - String with energy channel info
            - Value of lower energy bin edge in MeV
            - Value of energy bin width in MeV
    For STEP:
        1. Pandas dataframe with fluxes and errors in 'particles / (s cm^2 sr MeV)'
        2. Dictionary with energy information for all particles:
            - String with energy channel info
            - Value of lower energy bin edge in MeV
            - Value of energy bin width in MeV

    Raises
    ------
    Exception
        Sensors 'ept' or 'het' need a provided 'viewing' direction. If None is
        given, Exception is raised.

    Examples
    --------
    Load EPD/HET sun viewing direction low-latency data for Aug 20 to Aug 22,
    2020 from user-defined directory, downloading missing files from SOAR:

    >>> df_protons, df_electrons, energies = epd_load('het', 'll', 20200820,
    ...     20200822, 'sun', None, True)

    Load EPD/STEP level 2 data for Aug 20 to Aug 22, 2020 from user-defined
    directory, downloading missing files from SOAR:

    >>> df, energies = epd_load(sensor='step', level='l2', startdate=20200820,
    ... enddate=20200822, autodownload=True)
    """

    # refuse string as date input:
    for d in [startdate, enddate]:
        if isinstance(d, str):
            raise SystemExit("startdate & enddate must be datetime objects or YYYYMMDD integer!")

    # accept datetime object as date input by converting it to internal integer:
    if isinstance(startdate, dt.datetime) or isinstance(startdate, dt.date):
        startdate = int(startdate.strftime("%Y%m%d"))
    if isinstance(enddate, dt.datetime) or isinstance(enddate, dt.date):
        enddate = int(enddate.strftime("%Y%m%d"))

    # check integer date input for length:
    for d in [startdate, enddate]:
        if isinstance(d, int):
            if len(str(d)) != 8:
                raise SystemExit(f"startdate & enddate must be (datetime objects or) integers of the form YYYYMMDD, not {d}!")

    if sensor.lower() == 'step':
        datadf, energies_dict = \
            _read_step_cdf(level, startdate, enddate, path, autodownload, only_averages)
        return datadf, energies_dict
    if sensor.lower() == 'ept' or sensor.lower() == 'het':
        if viewing is None:
            raise Exception("EPT and HET need a telescope 'viewing' " +
                            "direction! No data read!")
            df_epd_p = []
            df_epd_e = []
            energies_dict = []
        else:
            df_epd_p, df_epd_e, energies_dict = \
                _read_epd_cdf(sensor, viewing, level, startdate, enddate, path,
                              autodownload)
        return df_epd_p, df_epd_e, energies_dict


def _read_epd_cdf(sensor, viewing, level, startdate, enddate=None, path=None,
                  autodownload=False):
    """
    INPUT:
        sensor: 'ept' or 'het' (string)
        viewing: 'sun', 'asun', 'north', or 'south' (string)
        level: 'll' or 'l2' (string)
        startdate,
        enddate:    YYYYMMDD, e.g., 20210415 (integer)
                    (if no enddate is given, 'enddate = startdate' will be set)
        path: directory in which Solar Orbiter data is/should be organized;
              e.g. '/home/userxyz/uni/solo/data/' (string)
        autodownload: if True will try to download missing data files from SOAR
    RETURNS:
        1. Pandas dataframe with proton fluxes and errors (for EPT also alpha
           particles) in 'particles / (s cm^2 sr MeV)'
        2. Pandas dataframe with electron fluxes and errors in
           'particles / (s cm^2 sr MeV)'
        3. Dictionary with energy information for all particles:
            - String with energy channel info
            - Value of lower energy bin edge in MeV
            - Value of energy bin width in MeV
    """

    # if no path to data directory is given, use the current directory
    if path is None:
        path = os.getcwd()

    # select sub-directory for corresponding sensor (EPT, HET)
    if level.lower() == 'll':
        path = Path(path)/'low_latency'/'epd'/sensor.lower()
    if level.lower() == 'l2':
        path = Path(path)/'l2'/'epd'/sensor.lower()

    # add a OS-specific '/' to end end of 'path'
    path = f'{path}{os.sep}'

    # if no 'enddate' is given, get data only for single day of 'startdate'
    if enddate is None:
        enddate = startdate

    # if autodownload, check online available files and download if not locally
    if autodownload:
        _autodownload_cdf(startdate, enddate, sensor.lower(), level.lower(),
                          path)

    # get list of local files for date range
    filelist = _get_epd_filelist(sensor.lower(), level.lower(), startdate,
                                 enddate, path=path)[viewing.lower()]

    # check for duplicate files with different version numbers and remove them
    filelist = _check_duplicates(filelist, verbose=True)

    if len(filelist) == 0:
        warnings.warn('WARNING: No corresponding data files found! Try different settings, path or autodownload.')
        df_epd_p = []
        df_epd_e = []
        energies_dict = []
    else:

        """ <-- get column names of dataframe """
        if sensor.lower() == 'ept':
            if level.lower() == 'll':
                protons = 'Prot'
                electrons = 'Ele'
                e_epoch = 0  # 'EPOCH'
            if level.lower() == 'l2':
                protons = 'Ion'
                electrons = 'Electron'
                e_epoch = 1  # 'EPOCH_1'
        if sensor.lower() == 'het':
            if level.lower() == 'll':
                protons = 'H'
                electrons = 'Ele'
                e_epoch = 0  # 'EPOCH'
            if level.lower() == 'l2':
                protons = 'H'  # EPOCH
                electrons = 'Electron'  # EPOCH_4, QUALITY_FLAG_4
                e_epoch = 4  # 'EPOCH_4'

        # load cdf files using read_cdf from sunpy (uses cdflib)
        data = read_cdf(filelist[0])
        df_p = data[0].to_dataframe()
        df_e = data[e_epoch].to_dataframe()

        if len(filelist) > 1:
            for f in filelist[1:]:
                data = read_cdf(f)
                t_df_p = data[0].to_dataframe()
                t_df_e = data[e_epoch].to_dataframe()
                df_p = pd.concat([df_p, t_df_p])
                df_e = pd.concat([df_e, t_df_e])

        # directly open first cdf file with cdflib to access metadata used in the following
        t_cdf_file = cdflib.CDF(filelist[0])

        # p intensities:
        flux_p_channels = \
            [protons+f'_Flux_{i}' for i in
             range(t_cdf_file.varinq(protons+'_Flux')['Dim_Sizes'][0])]
        # p errors:
        if level.lower() == 'll':
            flux_sigma_p_channels = \
                [protons+f'_Flux_Sigma_{i}' for i in
                 range(t_cdf_file.varinq(protons+'_Flux')['Dim_Sizes'][0])]
        if level.lower() == 'l2':
            flux_sigma_p_channels = \
                [protons+f'_Uncertainty_{i}' for i in
                 range(t_cdf_file.varinq(protons+'_Flux')['Dim_Sizes'][0])]
            # p rates:
            rate_p_channels = \
                [protons+f'_Rate_{i}' for i in
                 range(t_cdf_file.varinq(protons+'_Rate')['Dim_Sizes'][0])]

        if sensor.lower() == 'ept':
            # alpha intensities:
            flux_a_channels = \
                [f'Alpha_Flux_{i}' for i in
                 range(t_cdf_file.varinq("Alpha_Flux")['Dim_Sizes'][0])]
            # alpha errors:
            if level.lower() == 'll':
                flux_sigma_a_channels = \
                    [f'Alpha_Flux_Sigma_{i}' for i in
                     range(t_cdf_file.varinq("Alpha_Flux")['Dim_Sizes'][0])]
            if level.lower() == 'l2':
                flux_sigma_a_channels = \
                    [f'Alpha_Uncertainty_{i}' for i in
                     range(t_cdf_file.varinq("Alpha_Flux")['Dim_Sizes'][0])]
                # alpha rates:
                rate_a_channels = \
                    [f'Alpha_Rate_{i}' for i in
                     range(t_cdf_file.varinq("Alpha_Rate")['Dim_Sizes'][0])]

        # e intensities:
        flux_e_channels = \
            [electrons+f'_Flux_{i}' for i in
             range(t_cdf_file.varinq(electrons+'_Flux')['Dim_Sizes'][0])]
        # e errors:
        if level.lower() == 'll':
            flux_sigma_e_channels = \
                [f'Ele_Flux_Sigma_{i}' for i in
                 range(t_cdf_file.varinq(electrons+'_Flux')['Dim_Sizes'][0])]
        if level.lower() == 'l2':
            flux_sigma_e_channels = \
                [f'Electron_Uncertainty_{i}' for i in
                 range(t_cdf_file.varinq(electrons+'_Flux')['Dim_Sizes'][0])]
            # e rates:
            rate_e_channels = \
                [electrons+f'_Rate_{i}' for i in
                 range(t_cdf_file.varinq(electrons+'_Rate')['Dim_Sizes'][0])]

        if level.lower() == 'l2':
            if sensor.lower() == 'het':
                df_epd_p = pd.concat(
                    [df_p[flux_p_channels], df_p[flux_sigma_p_channels],
                     df_p[rate_p_channels], df_p['DELTA_EPOCH'],
                     df_p['QUALITY_FLAG'], df_p['QUALITY_BITMASK']],
                    axis=1,
                    keys=['H_Flux', 'H_Uncertainty', 'H_Rate',
                          'DELTA_EPOCH', 'QUALITY_FLAG', 'QUALITY_BITMASK'])

                df_epd_e = pd.concat([df_e[flux_e_channels],
                                      df_e[flux_sigma_e_channels],
                                      df_e[rate_e_channels],
                                      df_e['DELTA_EPOCH_4'],
                                      df_e['QUALITY_FLAG_4'],
                                      df_e['QUALITY_BITMASK_4']], axis=1,
                                     keys=['Electron_Flux',
                                           'Electron_Uncertainty',
                                           'Electron_Rate',
                                           'DELTA_EPOCH_4',
                                           'QUALITY_FLAG_4',
                                           'QUALITY_BITMASK_4'])

            if sensor.lower() == 'ept':
                df_epd_p = pd.concat(
                    [df_p[flux_p_channels], df_p[flux_sigma_p_channels],
                     df_p[rate_p_channels], df_p[flux_a_channels],
                     df_p[flux_sigma_a_channels], df_p[rate_a_channels],
                     df_p['DELTA_EPOCH'], df_p['QUALITY_FLAG'],
                     df_p['QUALITY_BITMASK']],
                    axis=1,
                    keys=['Ion_Flux', 'Ion_Uncertainty', 'Ion_Rate',
                          'Alpha_Flux', 'Alpha_Uncertainty', 'Alpha_Rate',
                          'DELTA_EPOCH', 'QUALITY_FLAG', 'QUALITY_BITMASK'])

                df_epd_e = pd.concat([df_e[flux_e_channels],
                                      df_e[flux_sigma_e_channels],
                                      df_e[rate_e_channels],
                                      df_e['DELTA_EPOCH_1'],
                                      df_e['QUALITY_FLAG_1'],
                                      df_e['QUALITY_BITMASK_1']], axis=1,
                                     keys=['Electron_Flux',
                                           'Electron_Uncertainty',
                                           'Electron_Rate',
                                           'DELTA_EPOCH_1',
                                           'QUALITY_FLAG_1',
                                           'QUALITY_BITMASK_1'])

        if level.lower() == 'll':
            if sensor.lower() == 'het':
                df_epd_p = pd.concat(
                    [df_p[flux_p_channels], df_p[flux_sigma_p_channels]],
                    axis=1, keys=['H_Flux', 'H_Uncertainty', 'QUALITY_FLAG'])

            if sensor.lower() == 'ept':
                df_epd_p = pd.concat(
                    [df_p[flux_p_channels], df_p[flux_sigma_p_channels],
                     df_p[flux_a_channels], df_p[flux_sigma_a_channels],
                     df_p['QUALITY_FLAG']],
                    axis=1, keys=['Ion_Flux', 'Ion_Uncertainty',
                                  'Alpha_Flux', 'Alpha_Uncertainty',
                                  'QUALITY_FLAG'])

            df_epd_e = pd.concat([df_e[flux_e_channels],
                                  df_e[flux_sigma_e_channels],
                                  df_e['QUALITY_FLAG']], axis=1,
                                 keys=['Electron_Flux',
                                       'Electron_Uncertainty',
                                       'QUALITY_FLAG'])

        # manual replace FILLVALUES in dataframes with np.nan
        # t_cdf_file.varattsget("Ion_Flux")["FILLVAL"][0] = -1e+31
        # same for l2 & ll and het & ept and e, p/ion, alpha
        # remove this (i.e. following two lines) when sunpy's read_cdf is updated,
        # and FILLVAL will be replaced directly, see
        # https://github.com/sunpy/sunpy/issues/5908
        # df_epd_p = df_epd_p.replace(np.float32(-1e+31), np.nan)
        # df_epd_e = df_epd_e.replace(np.float32(-1e+31), np.nan)
        # 1 Mar 2023: previous 2 lines removed because they are taken care of with sunpy
        # 4.1.0:
        # https://docs.sunpy.org/en/stable/whatsnew/changelog.html#id7
        # https://github.com/sunpy/sunpy/pull/5956

        energies_dict = {protons+"_Bins_Text":
                         t_cdf_file.varget(protons+'_Bins_Text'),
                         protons+"_Bins_Low_Energy":
                         t_cdf_file.varget(protons+'_Bins_Low_Energy'),
                         protons+"_Bins_Width":
                         t_cdf_file.varget(protons+'_Bins_Width'),
                         electrons+"_Bins_Text":
                         t_cdf_file.varget(electrons+'_Bins_Text'),
                         electrons+"_Bins_Low_Energy":
                         t_cdf_file.varget(electrons+'_Bins_Low_Energy'),
                         electrons+"_Bins_Width":
                         t_cdf_file.varget(electrons+'_Bins_Width')
                         }

        if sensor.lower() == 'ept':
            energies_dict["Alpha_Bins_Text"] = \
                t_cdf_file.varget('Alpha_Bins_Text')
            energies_dict["Alpha_Bins_Low_Energy"] = \
                t_cdf_file.varget('Alpha_Bins_Low_Energy')
            energies_dict["Alpha_Bins_Width"] = \
                t_cdf_file.varget('Alpha_Bins_Width')

        # name index column (instead of e.g. 'EPOCH' or 'EPOCH_1')
        df_epd_p.index.names = ['Time']
        df_epd_e.index.names = ['Time']

    '''
    Careful if adding more species - they might have different EPOCH
    dependencies and cannot easily be put in the same dataframe!
    '''

    return df_epd_p, df_epd_e, energies_dict


def _read_step_cdf(level, startdate, enddate=None, path=None, autodownload=False,
                   only_averages=False):
    """
    INPUT:
        level: 'll' or 'l2' (string)
        startdate,
        enddate:    YYYYMMDD, e.g., 20210415 (integer)
                    (if no enddate is given, 'enddate = startdate' will be set)
        path: directory in which Solar Orbiter data is/should be organized;
              e.g. '/home/userxyz/uni/solo/data/' (string)
        autodownload: if True will try to download missing data files from SOAR
        only_averages : bool, optional
            If True, will for STEP only return the averaged fluxes, and not the data
            of each of the 15 Pixels. This will reduce the memory consumption. By
            default False.
    RETURNS:
        1. Pandas dataframe with fluxes and errors in
           'particles / (s cm^2 sr MeV)'
        2. Dictionary with energy information for all particles:
            - String with energy channel info
            - Value of lower energy bin edge in MeV
            - Value of energy bin width in MeV
    """
    sensor = 'step'

    # if no path to data directory is given, use the current directory
    if path is None:
        path = os.getcwd()

    # select sub-directory for corresponding sensor (in this case just 'step')
    if level.lower() == 'll':
        path = Path(path)/'low_latency'/'epd'/sensor.lower()
    if level.lower() == 'l2':
        path = Path(path)/'l2'/'epd'/sensor.lower()

    # add a OS-specific '/' to end end of 'path'
    path = f'{path}{os.sep}'

    # if no 'enddate' is given, get data only for single day of 'startdate'
    if enddate is None:
        enddate = startdate

    # check if Oct 22 2021 is within time interval; at that date the data product changed!
    if startdate <= 20211022:
        product = 'rates'
    if startdate > 20211022:
        product = 'main'
    if startdate < 20211022 and enddate > 20211022:
        warnings.warn('WARNING: During the selected time range the STEP data product changed (on Oct 22 2021)! Please adjust time range and run again.')
        datadf = []
        energies_dict = []
    else:

        # if True, check online available files and download if not locally present
        if autodownload:
            _autodownload_cdf(startdate, enddate, sensor.lower(), level.lower(), path)

        # get list of local files for date range
        filelist = _get_step_filelist(level.lower(), startdate, enddate, path=path)

        # check for duplicate files with different version numbers and remove them
        filelist = _check_duplicates(filelist, verbose=True)

        if len(filelist) == 0:
            warnings.warn('WARNING: No corresponding data files found! Try different settings, path or autodownload.')
            datadf = []
            energies_dict = []
        elif product == 'rates':
            all_cdf = []
            for file in filelist:
                all_cdf.append(cdflib.CDF(file))

            if level == 'l2':
                param_list = ['Integral_Flux', 'Magnet_Flux', 'Integral_Rate',
                              'Magnet_Rate', 'Magnet_Uncertainty',
                              'Integral_Uncertainty']
                # set up the dictionary:
                energies_dict = \
                    {"Bins_Text": all_cdf[0].varget('Bins_Text'),
                     "Bins_Low_Energy": all_cdf[0].varget('Bins_Low_Energy'),
                     "Bins_Width": all_cdf[0].varget('Bins_Width'),
                     "Sector_Bins_Text": all_cdf[0].varget('Sector_Bins_Text'),
                     "Sector_Bins_Low_Energy": all_cdf[0].varget('Sector_Bins_Low_Energy'),
                     "Sector_Bins_Width": all_cdf[0].varget('Sector_Bins_Width')
                     }
            if level == 'll':
                param_list = ['Integral_Flux', 'Ion_Flux', 'Integral_Flux_Sigma',
                              'Ion_Flux_Sigma']
                # set up the dictionary:
                energies_dict = \
                    {"Integral_Bins_Text": all_cdf[0].varget('Integral_Bins_Text'),
                     "Integral_Bins_Low_Energy": all_cdf[0].varget('Integral_Bins_Low_Energy'),
                     "Integral_Bins_Width": all_cdf[0].varget('Integral_Bins_Width'),
                     "Ion_Bins_Text": all_cdf[0].varget('Ion_Bins_Text'),
                     "Ion_Bins_Low_Energy": all_cdf[0].varget('Ion_Bins_Low_Energy'),
                     "Ion_Bins_Width": all_cdf[0].varget('Ion_Bins_Width')
                     }

            df_list = []
            for cdffile in all_cdf:
                col_list = []
                for key in param_list:
                    try:
                        t_df = pd.DataFrame(cdffile[key], index=cdffile['EPOCH'])

                        # Replace FILLVAL dynamically for each element of param_list
                        fillval = cdffile.varattsget(key)["FILLVAL"]
                        t_df = t_df.replace(fillval, np.nan)

                        col_list.append(t_df)
                    except TypeError:
                        print(' ')
                        print("WARNING: Gap in dataframe due to missing cdf file.")
                        break
                try:
                    temp_df = pd.concat(col_list, axis=1, keys=param_list)
                    df_list.append(temp_df)
                except ValueError:
                    continue
            datadf = pd.concat(df_list)

            # transform the index of the dataframe into pd_datetime
            datetimes = cdflib.cdfepoch.encode(datadf.index.values)
            datadf.index = pd.to_datetime(datetimes)

            datadf.index.names = ['Time']

            # if type(contamination_threshold) == int:
            #     print("'contamination_threshold' not yet included for old STEP data (before Oct 22, 2021)!")

        elif product == 'main':
            datadf, energies_dict = _read_new_step_cdf(filelist, only_averages)

    '''
    Careful if adding more species - they might have different EPOCH
    dependencies and cannot easily be put in the same dataframe!
    '''

    return datadf, energies_dict


def _read_new_step_cdf(files, only_averages=False):
    """
    Function that reads in new format (since Oct 2021) STEP CDF 'files'.
    EPOCH_X dependent data is obtained as Pandas Dataframe via sunpy.
    Time-independent meta data is read in from the first cdf file via cdflib.
    """
    # read electron correction factors and meta data via cdflib
    cdf = cdflib.CDF(files[0])
    Electron_Flux_Mult = {'Electron_Avg_Flux_Mult': cdf['Electron_Avg_Flux_Mult']}
    # if not only_averages:
    for i in range(1, 16):
        Electron_Flux_Mult['Electron_'+str(i).rjust(2, '0')+'_Flux_Mult'] = cdf['Electron_'+str(i).rjust(2, '0')+'_Flux_Mult']
    # df_Electron_Flux_Mult = pd.DataFrame(Electron_Flux_Mult)  # get dataframe from dict - not needed atm.

    meta = {'Bins_Low_Energy': cdf['Bins_Low_Energy']}
    for i in ['Bins_Width', 'Bins_Text', 'Electron_Bins_Low_Energy', 'Electron_Bins_Width', 'Electron_Bins_Text', 'XYZ', 'XYZ_Pixels', 'XYZ_Labels', 'RTN_Labels']:
        meta[i] = cdf[i]

    meta['Electron_Flux_Mult'] = Electron_Flux_Mult

    meta['df_rtn_desc'] = cdf.varattsget('RTN')['CATDESC']
    # TODO: add to meta: 'Sector_Bins_Text', 'Sector_Bins_Low_Energy', 'Sector_Bins_Width' -- don't exist in new data product?

    del cdf

    # use sunpy to get Pandas DataFrame of EPOCH_X-dependent variables
    # data = TimeSeries(files, concatenate=True)
    # df = data.to_dataframe()
    # del(data)

    df = pd.DataFrame()
    for f in files:
        print('Loading', f)
        data = TimeSeries(f, concatenate=True)
        tdf = data.to_dataframe()
        all_columns = False
        if not all_columns:
            # print('dropping Rates from tdf')
            tdf.drop(columns=tdf.filter(like='Rate').columns, inplace=True)
        # drop per-Pixel data from tdf
        if only_averages:
            # print('dropping Pixels from tdf')
            drop_cols = ['Integral_0', 'Integral_1', 'Magnet_0', 'Magnet_1']
            for col in drop_cols:
                tdf.drop(columns=tdf.filter(like=col).columns, inplace=True)
        # print('merge dataframes...')
        df = pd.concat([df, tdf])
        del (data, tdf)

    # move RTN and HCI to different df's because they have different time indices
    # print('move RTN')
    df_rtn = df[['RTN_0', 'RTN_1', 'RTN_2']].dropna(how='all')
    df = df.drop(columns=['RTN_0', 'RTN_1', 'RTN_2']).dropna(how='all')  # remove lines only containing NaN's (all)
    # print('move HCI')
    df_hci = df[['HCI_Lat', 'HCI_Lon', 'HCI_R']].dropna(how='all')
    df = df.drop(columns=['HCI_Lat', 'HCI_Lon', 'HCI_R']).dropna(how='all')  # remove lines only containing NaN's (all)
    meta['df_rtn'] = df_rtn
    del df_rtn
    meta['df_hci'] = df_hci
    del df_hci

    """
    # what to do with this? not read in by sunpy because of multi-dimensionality. skip for now
    RTN_Pixels              (EPOCH_1, Pixels, dim1) float32 0.8412 ... -0.2708
                            CATDESC: 'Particle flow direction (unit vector) in RTN coordinates for each pixel'
    """
    meta['RTN_Pixels'] = 'CDF var RTN_Pixels (Particle flow direction (unit vector) in RTN coordinates for each pixel) left out as of now because it is multidimensional'

    """
    Electron_Flux calculation moved to own function that includes correct resampling. For Now, it should be called independently.
    df = calc_electrons(df, meta, contamination_threshold=contamination_threshold, only_averages=only_averages, resample=False)
    """

    # TODO: replace all negative values in dataframe with np.nan (applies for electron fluxes that get negative in their calculation)
    # ==> not needed any more after masking above?
    # df = df.mask(df < 0)

    # TODO: multi-index (or rather multi-column) dataframe like previous product?

    # df3['QUALITY_FLAG'] = df['QUALITY_FLAG']
    # df3['QUALITY_BITMASK'] = df['QUALITY_BITMASK']
    # df3['SMALL_PIXELS_FLAG'] = df['SMALL_PIXELS_FLAG']

    return df, meta


def calc_electrons(df, meta, contamination_threshold=2, only_averages=False, resample=False):
    """
    Calulate STEP electron data from Integral and Magnet observations.

    Parameters
    ----------
    df : Pandas DataFrame
        DataFrame containing the original STEP data read-in with epd_load
        (containing Integral_Fluxes and Magnet_Fluxes).
    meta : dict
        Dictionary of meta data like energy information provided as second output
        of epd_load.
    contamination_threshold : int or False/None, optional
        If int, mask electron data that probably is contaminated (i.e., set it
        to nan) using an integer contamination threshold following the equation:
        Integral_Flux - Magnet_Flux > contamination_threshold * Integral_Uncertainty
        If False, don't alter the data at all. Only implemented for new STEP
        data (after Oct 2021) so far. By default 2.
    only_averages : bool, optional
        If True, will for STEP only return the averaged fluxes, and not the data
        of each of the 15 Pixels. This will reduce the memory consumption. By
        default False.
    resample : str
        Pandas-readable resampling time, e.g. '1min'

    Returns
    -------
    df : Pandas DataFrame
        DataFrame sutrucuted as the input DataFrame, but with additional Electron columns
        (Flux and Uncertainity) and possibly resampled.
    """
    df = df.copy()

    Electron_Flux_Mult = meta['Electron_Flux_Mult']

    if resample:
        # for all Integral and Magnet Uncertainties:
        col_uncertainties = df.filter(like=f'_Uncertainty_').columns.tolist()
        for delta_flux in col_uncertainties:
            # overwrite x_Uncertainty with temp. variable x_Uncertainty**2 * dt**2 that is summed in the resampling
            df[delta_flux] = df[delta_flux]**2 * df['DELTA_EPOCH']**2

        # select columns that should be summed in the resampling process (instead of calculating the mean)
        col_sum = col_uncertainties.copy()
        col_sum.insert(0, 'DELTA_EPOCH')  # same as append, but puts it to the start of the list (not really necessary)

        # select columns for which the mean should be calculated in the resampling process.
        # do this by removing "to be summed" columns from the list of all columns.
        col_mean = df.columns.drop(col_sum).tolist()

        # build dictionary for agg function that defines how columns should be aggregated
        dict_agg = {}
        for c in col_sum:
            dict_agg[c] = 'sum'
        for c in col_mean:
            dict_agg[c] = 'mean'

        # resample with the timestamps at the beginning of the interval (like in original data!)
        df = df.resample(resample, origin='start', label="left").agg(dict_agg)

        # move timestamp to the center of each interval
        df.index = df.index + pd.tseries.frequencies.to_offset(pd.Timedelta(resample)/2)

        # calculate correctly resampled Uncertainties:
        for delta_flux in col_uncertainties:
            # delta_flux_resampled = np.sqrt( delta_flux_temp / dt^2 )  # delta_flux_temp and dt are resampled sums here!
            df[delta_flux] = np.sqrt(df[delta_flux] / df['DELTA_EPOCH']**2)

    # create list of electron fluxes to be calculated: only average or average + all individual pixels:
    if only_averages:
        pix_list = ['Avg']
    else:
        pix_list = ['Avg']+[str(n).rjust(2, '0') for n in range(1, 16)]

    # calculate electron fluxes from Magnet and Integral Fluxes using correction factors
    for i in range(len(Electron_Flux_Mult['Electron_Avg_Flux_Mult'])):  # 32 energy channels
        for pix in pix_list:  # Avg, pixel 01 - 15 (00 is background pixel)
            df[f'Electron_{pix}_Flux_{i}'] = Electron_Flux_Mult[f'Electron_{pix}_Flux_Mult'][i] * (df[f'Integral_{pix}_Flux_{i}'] - df[f'Magnet_{pix}_Flux_{i}'])
            df[f'Electron_{pix}_Uncertainty_{i}'] = \
                Electron_Flux_Mult[f'Electron_{pix}_Flux_Mult'][i] * np.sqrt(df[f'Integral_{pix}_Uncertainty_{i}']**2 + df[f'Magnet_{pix}_Uncertainty_{i}']**2)

            if type(contamination_threshold) == int:
                if contamination_threshold != 0:
                    clean = (df[f'Integral_{pix}_Flux_{i}'] - df[f'Magnet_{pix}_Flux_{i}']) > contamination_threshold*df[f'Integral_{pix}_Uncertainty_{i}']
                    # clean = (df[f'Integral_{pix}_Rate_{i}'] - df[f'Magnet_{pix}_Rate_{i}']) > contamination_threshold*np.sqrt(df[f'Integral_{pix}_Rate_{i}'])/np.sqrt(df['DELTA_EPOCH'])
                    # clean = (df[f'Integral_{pix}_Rate_{i}'] - df[f'Magnet_{pix}_Rate_{i}']) > contamination_threshold*np.sqrt(df[f'Integral_{pix}_Counts_{i}'])/df['DELTA_EPOCH']

                    # mask non-clean data
                    df[f'Electron_{pix}_Flux_{i}'] = df[f'Electron_{pix}_Flux_{i}'].mask(~clean)
                    df[f'Electron_{pix}_Uncertainty_{i}'] = df[f'Electron_{pix}_Uncertainty_{i}'].mask(~clean)

    if contamination_threshold == 0:
        print("contamination_threshold has been set to 0. Ignoring the contamination_threshold (i.e., NOT calculating it for 0)!")

    if type(contamination_threshold) != int:
        print("Info: contamination_threshold will only be applied if it is an integer. Otherwise only negative fluxes are removed.")

    # remove negative fluxes (probably not needed for masked data, but for contamination_threshold=None)
    df = df.mask(df < 0)

    return df


def _calc_electrons_rates(df, meta, contamination_threshold=2, only_averages=False, resample=False):
    """
    Outdated version of calc_electrons() that used rates to calculate counts, which are then used to calculate resampled uncertainties
    """
    df = df.copy()

    Electron_Flux_Mult = meta['Electron_Flux_Mult']

    for i in range(len(Electron_Flux_Mult['Electron_Avg_Flux_Mult'])):  # 32 energy channels
        # calculate Integral_xx_Counts_i (to be used with contamination threshold later)
        for pix in [str(n).rjust(2, '0') for n in range(1, 16)]:  # pixel 01 - 15 (00 is background pixel)
            df[f'Integral_{pix}_Counts_{i}'] = df[f'Integral_{pix}_Rate_{i}'] * df['DELTA_EPOCH']
            df[f'Magnet_{pix}_Counts_{i}'] = df[f'Magnet_{pix}_Rate_{i}'] * df['DELTA_EPOCH']

        # calculate Integral_Avg_Counts_i from sum of Integral_xx_Counts_i
        df[f'Integral_Avg_Counts_{i}'] = df.filter(like='Integral_').filter(like=f'_Counts_{i}').sum(axis=1)
        df[f'Magnet_Avg_Counts_{i}'] = df.filter(like='Magnet_').filter(like=f'_Counts_{i}').sum(axis=1)

        # calculate Integral_Avg_Rate_i from Integral_Avg_Counts_i and integration time
        df[f'Integral_Avg_Rate_{i}'] = df[f'Integral_Avg_Counts_{i}'] / df['DELTA_EPOCH']
        df[f'Magnet_Avg_Rate_{i}'] = df[f'Magnet_Avg_Counts_{i}'] / df['DELTA_EPOCH']

    if resample:
        # select columns that should be summed in the resampling process (instead of calculating the mean)
        col_sum = df.filter(like=f'_Counts_').columns.tolist()
        col_sum.insert(0, 'DELTA_EPOCH')  # same as append, but puts it to the start of the list (not really necessary)

        # select columns for which the mean should be calculated in the resampling process.
        # do this by removing "to be summed" columns from the list of all columns.
        col_mean = df.columns.drop(col_sum).tolist()

        # build dictionary for agg function that defines how columns should be aggregated
        dict_agg = {}
        for c in col_sum:
            dict_agg[c] = 'sum'
        for c in col_mean:
            dict_agg[c] = 'mean'

        # resample with the timestamps at the beginning of the interval (like in original data!)
        df = df.resample(resample, origin='start', label="left").agg(dict_agg)

        # move timestamp to the center of each interval
        df.index = df.index + pd.tseries.frequencies.to_offset(pd.Timedelta(resample)/2)

    # create list of electron fluxes to be calculated: only average or average + all individual pixels:
    if only_averages:
        pix_list = ['Avg']
    else:
        pix_list = ['Avg']+[str(n).rjust(2, '0') for n in range(1, 16)]

    # calculate electron fluxes from Magnet and Integral Fluxes using correction factors
    for i in range(len(Electron_Flux_Mult['Electron_Avg_Flux_Mult'])):  # 32 energy channels
        for pix in pix_list:  # Avg, pixel 01 - 15 (00 is background pixel)
            # print(f'Electron_{pix}_Flux_{i}', f"Electron_Flux_Mult['Electron_{pix}_Flux_Mult'][i]", f'Integral_{pix}_Flux_{i}', f'Magnet_{pix}_Flux_{i}')
            df[f'Electron_{pix}_Flux_{i}'] = Electron_Flux_Mult[f'Electron_{pix}_Flux_Mult'][i] * (df[f'Integral_{pix}_Flux_{i}'] - df[f'Magnet_{pix}_Flux_{i}'])

            df[f'Electron_{pix}_Uncertainty_{i}'] = \
                Electron_Flux_Mult[f'Electron_{pix}_Flux_Mult'][i] * np.sqrt(df[f'Integral_{pix}_Uncertainty_{i}']**2 + df[f'Magnet_{pix}_Uncertainty_{i}']**2)

            if type(contamination_threshold) == int:
                # clean = (df[f'Integral_{pix}_Flux_{i}'] - df[f'Magnet_{pix}_Flux_{i}']) > contamination_threshold*df[f'Integral_{pix}_Uncertainty_{i}']
                # clean = (df[f'Integral_{pix}_Rate_{i}'] - df[f'Magnet_{pix}_Rate_{i}']) > contamination_threshold*np.sqrt(df[f'Integral_{pix}_Rate_{i}'])/np.sqrt(df['DELTA_EPOCH'])
                clean = (df[f'Integral_{pix}_Rate_{i}'] - df[f'Magnet_{pix}_Rate_{i}']) > contamination_threshold*np.sqrt(df[f'Integral_{pix}_Counts_{i}'])/df['DELTA_EPOCH']

                # mask non-clean data
                df[f'Electron_{pix}_Flux_{i}'] = df[f'Electron_{pix}_Flux_{i}'].mask(~clean)
                df[f'Electron_{pix}_Uncertainty_{i}'] = df[f'Electron_{pix}_Uncertainty_{i}'].mask(~clean)

    # drop columns Rate and Counts from final df
    all_columns = False
    if not all_columns:
        df.drop(columns=df.filter(like='Rate').columns, inplace=True)
        df.drop(columns=df.filter(like='Counts').columns, inplace=True)
    return df


def _calc_electrons_old(df, meta, contamination_threshold=2, only_averages=False, resample=False):
    """
    Outdated original functionality to derive Electron Fluxes. Mask too many data when using contamination threshold because the Integral_Uncertainties are not calculated correctly in the resampling.
    """
    df = df.copy()

    # create list of electron fluxes to be calculated: only average or average + all individual pixels:
    if only_averages:
        pix_list = ['Avg']
    else:
        pix_list = ['Avg']+[str(n).rjust(2, '0') for n in range(1, 16)]

    Electron_Flux_Mult = meta['Electron_Flux_Mult']

    if resample:
        df = _resample_df_old(df=df, resample=resample)

    # calculate electron fluxes from Magnet and Integral Fluxes using correction factors
    for i in range(len(Electron_Flux_Mult['Electron_Avg_Flux_Mult'])):  # 32 energy channels
        for pix in pix_list:  # Avg, pixel 01 - 15 (00 is background pixel)
            # print(f'Electron_{pix}_Flux_{i}', f"Electron_Flux_Mult['Electron_{pix}_Flux_Mult'][i]", f'Integral_{pix}_Flux_{i}', f'Magnet_{pix}_Flux_{i}')
            df[f'Electron_{pix}_Flux_{i}'] = Electron_Flux_Mult[f'Electron_{pix}_Flux_Mult'][i] * (df[f'Integral_{pix}_Flux_{i}'] - df[f'Magnet_{pix}_Flux_{i}'])

            df[f'Electron_{pix}_Uncertainty_{i}'] = \
                Electron_Flux_Mult[f'Electron_{pix}_Flux_Mult'][i] * np.sqrt(df[f'Integral_{pix}_Uncertainty_{i}']**2 + df[f'Magnet_{pix}_Uncertainty_{i}']**2)

            if type(contamination_threshold) == int:
                clean = (df[f'Integral_{pix}_Flux_{i}'] - df[f'Magnet_{pix}_Flux_{i}']) > contamination_threshold*df[f'Integral_{pix}_Uncertainty_{i}']
                # mask non-clean data
                df[f'Electron_{pix}_Flux_{i}'] = df[f'Electron_{pix}_Flux_{i}'].mask(~clean)
                df[f'Electron_{pix}_Uncertainty_{i}'] = df[f'Electron_{pix}_Uncertainty_{i}'].mask(~clean)
    return df


def _resample_df_old(df, resample, pos_timestamp="center", origin="start"):
    """
    Resamples a Pandas Dataframe or Series to a new frequency.

    Parameters:
    -----------
    df : pd.DataFrame or pd.Series
            The dataframe or series to resample
    resample : str
            pandas-compatible time string, e.g., '1min', '2H' or '25s'
    pos_timestamp : str, default 'center'
            Controls if the timestamp is at the center of the time bin, or at the start of it
    origin : str, default 'start'
            Controls if the origin of resampling is at the start of the day (midnight) or at the first
            entry of the input dataframe/series

    Returns:
    ----------
    df : pd.DataFrame or Series, depending on the input
    """
    try:
        df = df.resample(resample, origin=origin, label="left").mean()
        if pos_timestamp == 'start':
            df.index = df.index
        else:
            df.index = df.index + pd.tseries.frequencies.to_offset(pd.Timedelta(resample)/2)
        # if pos_timestamp == 'stop' or pos_timestamp == 'end':
        #     df.index = df.index + pd.tseries.frequencies.to_offset(pd.Timedelta(resample))
    except ValueError:
        raise ValueError(f"Your 'resample' option of [{resample}] doesn't seem to be a proper Pandas frequency!")

    return df
