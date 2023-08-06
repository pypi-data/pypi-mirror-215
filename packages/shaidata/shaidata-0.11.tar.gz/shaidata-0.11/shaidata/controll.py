import time
import argparse
from ingestion.command_interface import CommandITF as Igt_ITF
from server.command_interface import CommandITF as Svr_ITF
from util.logger import Logger
import util.util as utils

prop = utils.get_prop()
log = Logger(prop).init_logger()
"""
    |-  Shinhan AI - Data Pipeline Controller   (C=Command)(A=Argument)(O=Optional Argument)
    |--------------------------------------------------------------------------------
    |--------------------------------------------------------------------------------
    |--------------------------------------------------------------------------------
    |--     ingestion                           (C)ingestion commands 
    |---------------------------User Interface---------------------------------------
    |----       add                             (C)ingestion 등록
    |------         ingestion.json              (A)ingestion 정보 파일
    |----       update                          (C)ingestion 수정
    |------         igt_id                      (A)ingestion ID
    |------         ingestion.json              (A)ingestion 정보 파일
    |----       delete                          (C)ingestion 삭제
    |------         igt_id                      (A)ingestion ID
    |----       list                            (C)ingestion 목록 조회
    |----       info                            (C)ingestion 정보 상세
    |------         igt_id                      (A)ingestion ID
    |----       exlist                          (C)ingestion 수행 목록 조회
    |------         igt_id                      (A)ingestion ID
    |------         -len                        (O)수행 목록 표시 갯수 (Default 20)
    |----       lastexinfo                      (C)ingestion 최근 수행 정보 상세
    |------         igt_id                      (A)ingestion ID
    |----       exinfo                          (C)ingestion 수행 정보 상세
    |------         igt_id                      (A)ingestion ID
    |------         igt_exe_num                 (A)ingestion exe number
    |------         -log                        (O)ingestion 수행 log 확인
    |---------------------------System Interface-------------------------------------
    |----       autoexe                         (C)ingestion 수행 대상 목록 추출 및 수행  <-- Oozie 에서 호출
    |----       autocheck                       (C)ingestion 수행중 목록 상태 변경       <-- Oozie 에서 호출
    |----       exelist                         (C)ingestion 수행 대상 목록 조회
    |----       exec                            (C)ingestion 수행
    |------         igt_id                      (A)ingestion ID
    |--------------------------------------------------------------------------------
    |--------------------------------------------------------------------------------
    |--------------------------------------------------------------------------------
    |--     server                              (C)Server commands 
    |----       add                             (C)Server 등록
    |------         server.json                 (A)Server 정보 파일
    |----       update                          (C)Server 수정
    |------         sv_alias                    (A)ingestion ID
    |------         server.json                 (A)Server 정보 파일
    |----       delete                          (C)Server 삭제
    |------         sv_alias                    (A)Server ID
    |----       list                            (C)Server 목록 조회
    |--------------------------------------------------------------------------------
    |--     datasource                          (C)datasource commands 
    |----       add                             (C)Server 등록
    |------         server.json                 (A)Server 정보 파일
    |--------------------------------------------------------------------------------
    |--     pipeline                            (C)pipeline commands 
    |--------------------------------------------------------------------------------
"""
parser = argparse.ArgumentParser(description='Shinhan AI - Data Pipeline Controller',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
sub_parser = parser.add_subparsers()
ingestion = sub_parser.add_parser("ingestion", help='ingestion commands')
server = sub_parser.add_parser("server", help='server commands')
datasource = sub_parser.add_parser("datasource", help='server commands')

if __name__ == '__main__':
    start_time = time.time()
    # ----------------------------------------------------------------------------------------
    # ------------------- Ingestion ----------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    ingestion_sub = ingestion.add_subparsers(dest='ingestion')
    
    ingestion_add = ingestion_sub.add_parser("add", help='ingestion 등록')
    ingestion_add.add_argument("ingestion.json", metavar='FILE',
                               type=argparse.FileType('rt', encoding=prop['general']['encoding']),
                               help='ingetsion 정보 파일',
                               action=Igt_ITF, logger=log, properties=prop, purpose="add")

    ingestion_update = ingestion_sub.add_parser("update", help='ingestion 수정')
    ingestion_update.add_argument("igt_id", help='ingetsion ID')
    ingestion_update.add_argument("ingestion", metavar='FILE',
                                  type=argparse.FileType('rt', encoding=prop['general']['encoding']),
                                  help='ingetsion 정보 파일',
                                  action=Igt_ITF, logger=log, properties=prop, purpose="update")
    

    ingestion_delete = ingestion_sub.add_parser("delete", help='ingestion 삭제')
    ingestion_delete.add_argument("igt_id", help='ingetsion ID',action=Igt_ITF, logger=log, properties=prop, purpose="delete")



    ingestion_list = ingestion_sub.add_parser("list", help='ingestion list')
    ingestion_list.add_argument("igt_count", help='ingetsion list count', type=int, default=80, nargs='*', action=Igt_ITF, logger=log, properties=prop, purpose="list")

    ingestion_info = ingestion_sub.add_parser("info", help='ingestion 정보 상세')
    ingestion_info.add_argument("igt_id", help='ingetsion ID',action=Igt_ITF, logger=log, properties=prop, purpose="info")

    ingestion_exec = ingestion_sub.add_parser("exec", help='ingestion 실행')
    ingestion_exec.add_argument("igt_id", help='ingetsion ID',action=Igt_ITF, logger=log, properties=prop, purpose="exec")


    ingestion_exlist = ingestion_sub.add_parser("exlist", help='ingestion 수행 목록 조회')
    ingestion_exlist.add_argument("igt_id", help='ingetsion ID')
    ingestion_exlist.add_argument('-len', type=int, default=20)


    ingestion_lastexinfo = ingestion_sub.add_parser("lastexinfo", help='ingestion 최근 수행 정보 상세')
    ingestion_lastexinfo.add_argument("igt_id", help='ingetsion ID')
    # ingestion_lastexinfo.set_defaults(func=ingestion_lastexinfo_func)

    ingestion_exlist = ingestion_sub.add_parser("exinfo", help='ingestion 수행 정보 상세')
    ingestion_exlist.add_argument("igt_id", help='ingetsion ID')
    ingestion_exlist.add_argument('igt_exe_num', help='ingestion exe number')
    ingestion_exlist.add_argument('-log', help='ingestion 수행 log 확인')
    # ingestion_exlist.set_defaults(func=ingestion_exlist_func)
    # ----------------------------------------------------------------------------------------
    # ------------------- Server ----------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    server_sub = server.add_subparsers(dest='server')

    server_add = server_sub.add_parser("add", help='server 등록')
    server_add.add_argument("server.json", metavar='FILE',
                            type=argparse.FileType('rt', encoding=prop['general']['encoding']),
                            help='server 정보 파일',
                            action=Svr_ITF, logger=log, properties=prop, purpose="add")

    server_update = server_sub.add_parser("update", help='server 수정')
    server_update.add_argument("server.json", help='server 정보 파일')

    server_delete = server_sub.add_parser("delete", help='server 삭제')
    server_delete.add_argument("svr_alias", help='server alias',action=Svr_ITF, logger=log, properties=prop, purpose="delete")

    server_info = server_sub.add_parser("info", help='alias 정보 상세')
    server_info.add_argument("svr_alias", help='server alias',action=Svr_ITF, logger=log, properties=prop, purpose="info")


    server_list = server_sub.add_parser("list", help='server list')
    server_list.add_argument("server_display_max_count", help='server list count', type=int, default=80, nargs='*', action=Svr_ITF, logger=log, properties=prop, purpose="list")

    server_update = server_sub.add_parser("update", help='ingestion 수정')
    server_update.add_argument("sv_alias", help='server alias')
    server_update.add_argument("server", metavar='FILE',
                                  type=argparse.FileType('rt', encoding=prop['general']['encoding']),
                                  help='server 정보 파일',
                                  action=Svr_ITF, logger=log, properties=prop, purpose="update")


    # server_list.set_defaults(func=server_list_func)
    # ----------------------------------------------------------------------------------------
    # ------------------- data source --------------------------------------------------------
    # ----------------------------------------------------------------------------------------

    vendor = sub_parser.add_parser("vendor", help='vendor commands')
    vendor_sub = vendor.add_subparsers()
    # ----------------------------------------------------------------------------------------
    # ------------------- pipeline ----------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    pipeline = sub_parser.add_parser("pipeline", help='pipeline commands')
    pipeline_sub = pipeline.add_subparsers()
    # ----------------------------------------------------------------------------------------




    args = parser.parse_args()
    #print('[Debug1]:',args)

    if vars(args) == {}:
        parser.print_help()
    elif 'ingestion' in vars(args):
        if vars(args)['ingestion'] is None:
            ingestion.print_help()
            
