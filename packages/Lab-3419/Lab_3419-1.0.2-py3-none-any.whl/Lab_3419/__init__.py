import numpy as np
from multiprocessing import Pool


# Point in 3D  ---> point = (x, y, z)
# Points in 3D ---> line points = numpy.array([(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)])
# Line in 3D   ---> line = numpy.array([(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)])
# Fiited line  ---> line = numpy.array([(x1, y1, z1), (x2, y2, z2)])


def add_resolusion(points_, res_=0.0):
    data_x_, data_y_, data_z_ = points_.T
    data_x_e_ = data_x_ + np.random.normal(0, res_, len(data_x_))
    data_y_e_ = data_y_ + np.random.normal(0, res_, len(data_y_))
    # data_z_e_ = data_z_ + np.random.normal(0, res_, len(data_z_))
    data_z_e_ = data_z_
    data_xyz_e_ = np.array([data_x_e_, data_y_e_, data_z_e_]).T
    return data_xyz_e_

def find_angle(track_1, track_2):
    cos_theta_ = np.dot(track_1, track_2) / (np.linalg.norm(track_1) * np.linalg.norm(track_2))
    theta_rad_ = np.arccos(np.clip(cos_theta_, -1.0, 1.0))
    theta_deg_ = np.rad2deg(theta_rad_)
    return theta_deg_

def check_tracklets(points_):
    tracklet_1 = points_[0] - points_[1]
    tracklet_2 = points_[1] - points_[2]
    tracklet_3 = points_[0] - points_[2]
    tracklet_4 = points_[3] - points_[4]
    tracklet_5 = points_[4] - points_[5]
    tracklet_6 = points_[3] - points_[5]
    theta_1 = find_angle(tracklet_1, tracklet_2)
    theta_2 = find_angle(tracklet_2, tracklet_3)
    theta_3 = find_angle(tracklet_1, tracklet_3)
    theta_4 = find_angle(tracklet_4, tracklet_5)
    theta_5 = find_angle(tracklet_5, tracklet_6)
    theta_6 = find_angle(tracklet_4, tracklet_6)
    theta_tracklet = max(theta_1, theta_2, theta_3, theta_4, theta_5, theta_6)
    return theta_tracklet

def fit_3D(points_):
    data_x_, data_y_, data_z_ = points_.T
    fit_z_ = np.array([data_z_[0], data_z_[-1]])
    m_zx_, c_zx_, *_ = np.polyfit(data_z_, data_x_, 1)
    m_zy_, c_zy_, *_ = np.polyfit(data_z_, data_y_, 1)
    fit_x_ = m_zx_ * fit_z_ + c_zx_
    fit_y_ = m_zy_ * fit_z_ + c_zy_
    fit_xyz_ = np.array([fit_x_, fit_y_, fit_z_]).T
    return fit_xyz_


def fit_3D_with_parameters(points_):
    data_x_, data_y_, data_z_ = points_.T
    fit_z_ = np.array([data_z_[0], data_z_[-1]])
    m_zx_, c_zx_, *_ = np.polyfit(data_z_, data_x_, 1)
    m_zy_, c_zy_, *_ = np.polyfit(data_z_, data_y_, 1)
    fit_x_ = m_zx_ * fit_z_ + c_zx_
    fit_y_ = m_zy_ * fit_z_ + c_zy_
    fit_xyz_ = np.array([fit_x_, fit_y_, fit_z_]).T
    fit_params_ = {'line': fit_xyz_, 'm_zx': m_zx_, 'c_zx': c_zx_, 'm_zy': m_zy_, 'c_zy': c_zy_}
    return fit_params_


def POCA_Point(line_1_, line_2_):
    P0_, P1_ = line_1_[0], line_1_[1]
    Q0_, Q1_ = line_2_[0], line_2_[1]
    u_, v_, w_ = (P1_ - P0_), (Q1_ - Q0_), (P0_ - Q0_)
    cos_theta_ = np.dot(u_, v_) / (np.linalg.norm(u_) * np.linalg.norm(v_))
    theta_rad_ = np.arccos(np.clip(cos_theta_, -1.0, 1.0))
    theta_deg_ = np.rad2deg(theta_rad_)
    a_, b_, c_ = np.dot(u_, u_), np.dot(u_, v_), np.dot(v_, v_)
    d_, e_, f_ = np.dot(u_, w_), np.dot(v_, w_), (a_ * c_ - b_ * b_)
    if f_ == 0.0: f_ = 1.0e-10  # to avoid zero division error
    sc_, tc_ = (b_ * e_ - c_ * d_) / f_, (a_ * e_ - b_ * d_) / f_
    M1_, M2_ = (P0_ + sc_ * u_), (Q0_ + tc_ * v_)
    M_ = (M1_ + M2_) / 2.0
    return M_, theta_deg_


def POCA_Point_with_parameters(line_1_, line_2_):
    P0_, P1_ = line_1_[0], line_1_[1]
    Q0_, Q1_ = line_2_[0], line_2_[1]
    u_, v_, w_ = (P1_ - P0_), (Q1_ - Q0_), (P0_ - Q0_)
    cos_theta_ = np.dot(u_, v_) / (np.linalg.norm(u_) * np.linalg.norm(v_))
    theta_rad_ = np.arccos(np.clip(cos_theta_, -1.0, 1.0))
    theta_deg_ = np.rad2deg(theta_rad_)
    a_, b_, c_ = np.dot(u_, u_), np.dot(u_, v_), np.dot(v_, v_)
    d_, e_, f_ = np.dot(u_, w_), np.dot(v_, w_), (a_ * c_ - b_ * b_)
    if f_ == 0.0: f_ = 1.0e-10  # to avoid zero division error
    sc_, tc_ = (b_ * e_ - c_ * d_) / f_, (a_ * e_ - b_ * d_) / f_
    M1_, M2_ = (P0_ + sc_ * u_), (Q0_ + tc_ * v_)
    M12_ = np.linalg.norm(M2_ - M1_)
    M_ = (M1_ + M2_) / 2.0
    poca_params_ = {'poca': M_, 'deviation': theta_deg_, 'poca_1': M1_, 'poca_2': M2_, 'poca_gap': M12_}
    return poca_params_


def calculate(data_, sigma_=0.100):
    data_c_ = np.array([float(_) for _ in data_.split()])
    data_c_ = data_c_[0:18]
    rpc_hits_ = data_c_.reshape(6, 3)
#    sigma_ = 0.100
    rpc_hits_ = add_resolusion(rpc_hits_, sigma_)
    top_hits_, bottom_hits_ = rpc_hits_[0:3], rpc_hits_[3:6]
    top_line_ = fit_3D(top_hits_)
    bottom_line_ = fit_3D(bottom_hits_)
    (xp_, yp_, zp_), theta_deg_ = POCA_Point(top_line_, bottom_line_)
    return xp_, yp_, zp_, theta_deg_


def calculate_with_parameters(data_, sigma_=0.100):
    data_c_ = np.array([float(_) for _ in data_.split()])
    data_c_ = data_c_[0:18]
    rpc_hits_ = data_c_.reshape(6, 3)
    # sigma_ = 0.100
    rpc_hits_ = add_resolusion(rpc_hits_, sigma_)
    top_hits_, bottom_hits_ = rpc_hits_[0:3], rpc_hits_[3:6]
    top_line_ = fit_3D_with_parameters(top_hits_)
    bottom_line_ = fit_3D_with_parameters(bottom_hits_)
    (xp_, yp_, zp_), theta_deg_ = POCA_Point_with_parameters(top_line_, bottom_line_)
    return xp_, yp_, zp_, theta_deg_


def file_to_poca(file_name_, is_save=False):
    file_i_ = open(file_name_, 'r')
    data_file_ = file_i_.readlines()
    file_i_.close()
    print('Process started...')
    all_poca_data_ = []
    for line_ in data_file_:
        poca_data_ = calculate(line_)
        all_poca_data_.append(poca_data_)
    print('Reading Complited...')
    all_poca_data_ = np.array(all_poca_data_)
    if is_save:
        print('Saving Data...')
        np.savetxt(file_name_[:-4] + '_poca_points.txt', all_poca_data_, fmt='%.4f')
    print('Analysis Complited...')
    return all_poca_data_


def file_to_poca_mt(file_name_, is_save=False):
    file_i_ = open(file_name_, 'r')
    data_file_ = file_i_.readlines()
    file_i_.close()
    print('Process started...')
    process_pool_ = Pool()
    all_poca_data_ = process_pool_.map(calculate, data_file_)
    process_pool_.close()
    process_pool_.join()
    print('Reading Complited. ..')
    all_poca_data_ = np.array(all_poca_data_)
    if is_save:
        print('Saving Data...')
        np.savetxt(file_name_[:-4] + '_poca_points.txt', all_poca_data_, fmt='%.4f')
    print('Analysis Complited...')
    return all_poca_data_


def filter_poca_data(poca_data_, min_theta_):
    filter_data_ = []
    for xp_, yp_, zp_, theta_deg_ in poca_data_:
        if theta_deg_ < min_theta_: continue
        filter_data_.append([xp_, yp_, zp_, theta_deg_])
    filter_data_ = np.array(filter_data_)
    return filter_data_
