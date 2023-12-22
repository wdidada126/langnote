# github_codeql

https://codeql.github.com/


  Disabling C++ automatic installation of dependencies.
  /opt/hostedtoolcache/CodeQL/2.15.4/x64/codeql/cpp/tools/autobuild.sh 
  
  cpp/autobuilder: At least these two subdirs have build system files in them:
  cpp/autobuilder:   ./libodb-2.4.0
  cpp/autobuilder:   ./libodb-mysql-2.4.0
  cpp/autobuilder: To avoid ambiguity, build will be attempted from '.'
  cpp/autobuilder: even though no build system was found there.
  
  ~/work/odb/odb ~/work/odb/odb
  ~/work/odb/odb
  cpp/autobuilder: Incompatible operating system (expected Windows).
  cpp/autobuilder: No supported build system detected.
  Error: We were unable to automatically build your code. Please replace the call to the autobuild action with your custom build steps. Encountered a fatal error while running "/opt/hostedtoolcache/CodeQL/2.15.4/x64/codeql/cpp/tools/autobuild.sh". Exit code was 1 and last log line was: cpp/autobuilder: No supported build system detected. See the logs for more details.
  